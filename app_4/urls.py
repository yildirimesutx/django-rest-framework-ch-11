from django.urls import path
from .views import (
  
    StudentMVS,
)

from rest_framework import routers
router = routers.DefaultRouter()
# router = routers.SimpleRouter() iki farklı router var, simple da tek url çıkmıyor
router.register("api",StudentMVS)



urlpatterns = [
    # path('list', TodoList.as_view()),
    # path("detail/<int:id>", TodoDetail.as_view())
    # path("list", TodoListCreate.as_view()),
    # path("detail/<int:id>", TodoGetUpdateDelete.as_view()),
    # path("api" include(router.urls))
   
]

urlpatterns += router.urls
