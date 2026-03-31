from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions import IsOwner

from source.models import Source
from source.serializers import SourceSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsOwner])
def source_list(request):
  
    if request.method == "GET":
        company = request.user.subscriber.company_id
        sources = (
            Source.objects.select_related("company","created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .filter(company=company)
        )

        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
            company=request.user.subscriber.company_id,
            created_by=request.user,
            updated_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsOwner])
def source_detail(request, source_id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        source = Source.objects.get(id=source_id)
    except Source.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SourceSerializer(source)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = SourceSerializer(source, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 