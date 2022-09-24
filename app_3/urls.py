from django.urls import path
from .views import (
    # TodoDetail,
    # TodoList,
    # TodoListCreate,
    # TodoGetUpdateDelete
    TodoMVS,
    CategoryListCreate,
    CategoryGetUpdateDelete

)

from rest_framework import routers
router = routers.DefaultRouter()
# router = routers.SimpleRouter() iki farklı router var, simple da tek url çıkmıyor
router.register("todos",TodoMVS)



urlpatterns = [
    # path('list', TodoList.as_view()),
    # path("detail/<int:id>", TodoDetail.as_view())
    # path("list", TodoListCreate.as_view()),
    # path("detail/<int:id>", TodoGetUpdateDelete.as_view()),
    # path("api" include(router.urls))
    path("category/",CategoryListCreate.as_view()),
    path("category/<int:id>", CategoryGetUpdateDelete.as_view())
   
]

urlpatterns += router.urls
