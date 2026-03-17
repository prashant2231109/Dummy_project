from django.urls import path, include

from . import views

app_name = "source"

urlpatterns = [
    path("", views.fetch_sources, name="list"),
    path("add/", views.create_or_update, name="add"),
    path("update/<int:source_id>/", views.create_or_update, name="update"),
    path("delete/<int:source_id>/", views.delete, name="delete"),
    
  
]
