from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from permissions import IsOwner

from story.models import Story
from story.serializers import StorySerializer


class StoryList(generics.ListCreateAPIView):
    def get_queryset(self):
        company = self.request.user.subscriber.company_id

        return (
            Story.objects.select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .filter(company=company)
        )

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.subscriber.company_id,
            created_by=self.request.user
        )


class StoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        company = self.request.user.subscriber.company_id
        return (
            Story.objects.select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies").filter(company=company)
        )
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
   