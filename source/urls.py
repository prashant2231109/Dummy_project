from django.urls import path, include
from rest_framework.routers import DefaultRouter

from source import views

app_name = "source"

urlpatterns = [
    path("", views.fetch_sources, name="list"),
    path("add/", views.create_or_update, name="add"),
    path("update/<int:source_id>/", views.create_or_update, name="update"),
    path("delete/<int:source_id>/", views.delete_source, name="delete"),
]
