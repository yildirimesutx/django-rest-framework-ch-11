
from django.urls import path
from .views import StudentList, StudentOperations, logout_view

from rest_framework.authtoken import views

from .views import RegisterView

urlpatterns = [
    path('student/', StudentList.as_view()),
    path("student/<int:id>", StudentOperations.as_view(), name="detail"),
    path('login/', views.obtain_auth_token, name='login'),
    path("register/", RegisterView.as_view(), name="register" ),
     path('logout/', logout_view, name="logout"),
]