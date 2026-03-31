from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsOwner

from story.models import Story
from story.serializers import StorySerializer


class StoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, story_id=None):
        company = request.user.subscriber.company_id
        if story_id:
            try:
                story = Story.objects.get(id=story_id)
            except Story.DoesNotExist:
                return Response({"message": "id not found"})
            serializer = StorySerializer(story)
            return Response(serializer.data, status=status.HTTP_200_OK)

        stories = (
            Story.objects.select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .filter(company=company)
        )
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = StorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                updated_by=request.user,
                company=request.user.subscriber.company_id,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, story_id):
        if story_id:
            try:
                story = Story.objects.get(id=story_id)
                serializer = StorySerializer(instance=story, data=request.data)
                if serializer.is_valid():
                    serializer.save(updated_by=request.user)
                    return Response(serializer.data)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            except Story.DoesNotExist:
                return Response({"message": "source not found"})

        return Response({"message": "provide source id"})

    def delete(self, request, story_id):
        if story_id:
            try:
                story = Story.objects.get(id=story_id)
                story.delete()
                return Response(
                    {"message": "Story deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Story.DoesNotExist:
                return Response(
                    {"message": "Story not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"message": "provide story id"}, status=status.HTTP_400_BAD_REQUEST
        )
