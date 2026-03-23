from django.urls import path, include
from rest_framework.routers import DefaultRouter

from source.drf import viewsets, apiviews, functionals, generics

router = DefaultRouter()
router.register(r"viewsets" , viewsets.SourceViewSet , basename="viewset")

urlpatterns = [
    path("apiview/", apiviews.SourceAPIView.as_view(), name="api-list"),
    path("apiview/<int:source_id>/", apiviews.SourceAPIView.as_view(), 
        name="api-detail"),

    path("functional/", functionals.source_list),
    path("functional/<int:source_id>/", functionals.source_detail),  

    path('generic/', generics.SourceList.as_view(), name='source-list'),
    path('generic/<int:source_id>/', generics.SourceDetail.as_view(),
        name='source-detail'),

    path("", include(router.urls)),
]