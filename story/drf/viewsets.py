from rest_framework import permissions, viewsets


from permissions import IsOwner

from story.models import Story
from story.serializers import StorySerializer


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


    
    def get_queryset(self):
        
    
        company = self.request.user.subscriber.company
        return (
            Story.objects.select_related(
                "company", "created_by", "updated_by", "source"
            )
            .prefetch_related("tagged_companies", "source__tagged_companies")
            .filter(company=company)
        )
        

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.subscriber.company,
            created_by=self.request.user,
            updated_by=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
