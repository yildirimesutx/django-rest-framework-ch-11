from django.urls import path
from .views import student_api, student_api_get_update_delete,path_api 

urlpatterns = [
    path("students/", student_api),
    path("students/<int:pk>", student_api_get_update_delete),
    path("paths/", path_api)
]