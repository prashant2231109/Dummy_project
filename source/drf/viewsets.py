from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from permissions import IsOwner

from source.models import Source
from source.serializers import SourceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()

        return Source.objects.all()

    def perform_create(self, serializer):

        serializer.save(
            company=self.request.user.subscriber.company_id,
            created_by=self.request.user,
            updated_by=self.request.user,
        )

    def perform_update(self, serializer):

        serializer.save(updated_by=self.request.user)
