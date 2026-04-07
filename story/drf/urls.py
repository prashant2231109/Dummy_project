from django.urls import include, path
from rest_framework.routers import DefaultRouter

from story.drf import apiviews, functionals, generics, viewsets


router = DefaultRouter()
router.register(r"viewsets", viewsets.StoryViewSet, basename="viewset")


urlpatterns = [
    path("apiview/", apiviews.StoryAPIView.as_view(), name="api-list"),
    path("apiview/<int:source_id>/", apiviews.StoryAPIView.as_view(), 
    name="api-detail"),

    path("functional/", functionals.story_list),
    path("functional/<int:story_id>/", functionals.story_detail),  

    path('generic/', generics.StoryList.as_view(), name='source-list'),
    path('generic/<int:story_id>/', generics.StoryDetail.as_view(), name='source-detail'),
    
    path("", include(router.urls))  ,
  
]
