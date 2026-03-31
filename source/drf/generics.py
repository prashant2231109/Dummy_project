from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from permissions import IsOwner

from source.models import Source
from source.serializers import SourceSerializer


class SourceList(generics.ListCreateAPIView):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user_company = self.request.user.subscriber.company_id

        return (
            Source.objects.select_related(
                "company", "created_by", "updated_by"
            )
            .prefetch_related("tagged_companies")
            .filter(company=user_company)
        )

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.subscriber.company_id,
            created_by=self.request.user,
        )


class SourceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        company = self.request.user.subscriber.company_id
        return (
            Source.objects.select_related(
                "company", "created_by", "updated_by"
            )
            .prefetch_related("tagged_companies")
            .filter(company=company)
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
