from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework import filters
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from permissions import IsOwner

from source.models import Source
from source.serializers import SourceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'url'] 

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
        company = self.request.user.subscriber.company
        return (
            Source.objects.select_related("company","created_by", "updated_by")
            .prefetch_related("tagged_companies")
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


    def get_serializer_context(self):
        return {"request": self.request}     
