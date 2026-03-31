from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions import IsOwner

from story.models import Story
from story.serializers import StorySerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsOwner])
def story_list(request):
  
    if request.method == "GET":
        company = request.user.subscriber.company_id
        stories = (
            Story.objects.select_related("company","created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .filter(company=company)
        )
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                company=request.user.subscriber.company_id,
                created_by=request.user,
                updated_by=request.user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsOwner])
def story_detail(request, story_id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StorySerializer(story)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = StorySerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 