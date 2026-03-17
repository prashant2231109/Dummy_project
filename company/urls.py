from django.urls import path

app_name = "company"

from company.models import Company
from company import views

urlpatterns = [
   path("add/", views.add, name="add"),
   path("search", views.CompanyAutocomplete.as_view(), 
    name="search"),
]