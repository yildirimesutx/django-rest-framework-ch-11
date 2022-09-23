
from django.urls import path
from .views import StudentList, StudentOperations, logout_view

from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView

urlpatterns = [
    path('student/', StudentList.as_view()),
    path("student/<int:id>", StudentOperations.as_view(), name="detail"),
    path('login/', obtain_auth_token, name="login"),
    path("register/", RegisterView.as_view(), name="register" ),
     path('logout/', logout_view, name="logout"),
]