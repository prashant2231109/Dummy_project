from django.urls import path


from company.drf import functional

urlpatterns = [
    path("list/", functional.company_view, name="company"),
 
]