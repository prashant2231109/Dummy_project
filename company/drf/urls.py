from django.urls import path


from company.drf import functional

app_name = "company"

urlpatterns = [
    path("list/", functional.company_view, name="company"),
 
]