from django.urls import path, include

from . import views

app_name = "source"

urlpatterns = [
    path("",views.source_list,name="list"),
    path('add/', views.add_source, name='add'),
    path('update/<int:source_id>/', views.source_update, name='update'),
    path('delete/<int:source_id>/', views.source_delete, name='delete'),
    path('<int:source_id>/', views.source_detail, name='detail'),
]