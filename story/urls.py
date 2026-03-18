from django.urls import path, include

from . import views

app_name = "story"

urlpatterns = [
    path("", views.fetch_stories, name="list"),
    path("create/", views.create_or_update, name="create"),
    path("update/<int:story_id>/", views.create_or_update, name="update"),
    path("delete/<int:story_id>/", views.delete_story, name="delete"),
    path("search/", views.SourceAutocomplete.as_view(), name="search"),
  
]
