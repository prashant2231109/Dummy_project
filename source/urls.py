from django.urls import path, include

from . import views

app_name = "source"

urlpatterns = [
    path("", views.source_list, name="list"),
    path("add/", views.source_form, name="add"),
    path("update/<int:source_id>/", views.source_form, name="update"),
    path("delete/<int:source_id>/", views.source_delete, name="delete"),
    path("<int:source_id>/", views.source_detail, name="detail"),
    path("search/", views.source_search, name="search"),
    path("company-autocomplete/", views.CompanyAutocomplete.as_view(), 
    name="company-autocomplete"),
]
