from django.urls import path
from .views import hello_world, todoList, todoCreate, todoListCreate, todoUpdate, todoDelete


urlpatterns = [
    path('', hello_world),
    path("todoList/", todoList),
    path("todoCreate", todoCreate),
    path("todoAll", todoListCreate),
    path("todoUpdate/<int:pk>", todoUpdate),
    path("todoDelete/<int:pk>", todoDelete)
  
]