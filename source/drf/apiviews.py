from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsOwner

from source.models import Source
from source.serializers import SourceSerializer


class SourceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, source_id=None):
        if source_id:
            try:
                source = Source.objects.get(id=source_id)
            except Source.DoesNotExist:
                return Response({"message": "id not found"})
            serializer = SourceSerializer(source)
            return Response(serializer.data, status=status.HTTP_200_OK)

        sources = (
            Source.objects.select_related("company","created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .all()
        )
        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = SourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                updated_by=request.user,
                company=request.user.subscriber.company,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, source_id):
        if source_id:
            try:
                source = Source.objects.get(id=source_id)
                serializer = SourceSerializer(
                    instance=source, data=request.data
                )
                if serializer.is_valid():
                    serializer.save(updated_by=request.user)
                    return Response(serializer.data)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            except Source.DoesNotExist:
                return Response({"message": "source not found"})

        return Response({"message": "provide source id"})
