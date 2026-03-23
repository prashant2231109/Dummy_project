from rest_framework import permissions, viewsets

from permissions import IsOwner

from source.models import Source
from source.serializers import SourceSerializer

class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        company = self.request.user.subscriber.company_id

        return (
            Source.objects.select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies").filter(company=company)
        )

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.subscriber.company_id,
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
