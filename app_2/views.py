from django.shortcuts import render

# Create your views here.
from .models import Todo
from .serializers import  TodoSerializers


from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(["GET"])
def todoList(request):
    queryset = Todo.objects.all()
    print("q",queryset)
    
    serializer = TodoSerializers(queryset, many=True)

    print("s",serializer)


    return Response(serializer.data)



@api_view(["POST"])
def todoCreate(request):
    serializer= TodoSerializers(data=request.data)


    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK) 




@api_view(["GET","POST"])
def todoListCreate(request):
    if request.method == 'GET':
        todo = Todo.objects.all()

        serializer = TodoSerializers(todo, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer =   TodoSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



@api_view(["GET","PUT", "DELETE"])
def todoUpdate(request, pk):

    queryset = Todo.objects.get(id=pk)

    if request.method == "GET":
        serializer = TodoSerializers(queryset)
        
        return Response(serializer.data)



    elif request.method == "PUT":

        serializer = TodoSerializers(instance= queryset, data=request.data)
        
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND) 


    elif request.method == "DELETE":
        queryset.delete()
        return Response("item deleted")       





@api_view(["DELETE"])
def todoDelete(request, pk):
    queryset = Todo.objects.get(id=pk)
    queryset.delete()

    return Response("Item Deleted")







