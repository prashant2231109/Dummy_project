from django.urls import path, include

from . import views

app_name = "story"

urlpatterns = [
    path("", views.story_list, name="list"),
    path("create/", views.story_form, name="create"),
    path("<int:story_id>/", views.story_detail, name="story_detail"),
    path("update/<int:story_id>/", views.story_form, name="update"),
    path("delete/<int:story_id>/", views.story_delete, name="delete"),
    path("company-autocomplete/",views.CompanyAutocomplete.as_view(),
        name="company-autocomplete",
    ),
    path("search/", views.story_search, name="search")
    
]
