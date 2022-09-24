from django.shortcuts import render, get_object_or_404

from .models import Todo, Category
from .serializers import TodoSerializers, CategorySerializers

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins, viewsets
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import action


# class TodoList(APIView):

#     # def get_obj(self, id):
#     #     todo = get_object_or_404(Todo, id =id)

#     def get(self, request, id):  #buradaki get APIViewsden gelen source kodundan gelen method olduğundan isim değişikliği uygun değil
#         todo = Todo.objects.all()
#         # todo = self.get_obj(id)
#         serializer = TodoSerializers(todo, many=True)
#         return Response(serializer.data)


#     def post(self, request):
#         serializer = TodoSerializers(data=request.data)
#         if serializer.is_valid():
#            serializer.save()
#         return Response(serializer.data)

# class TodoDetail(APIView):

#     def get(self, request, id):
#         todo = Todo.objects.get(id=id)
#         serializer = TodoSerializers(todo)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         todo = Todo.objects.get(id=id)
#         serializer = TodoSerializers(instance=todo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         todo = Todo.objects.get(id=id)
#         todo.delete()

#         data = {
#             "message":"Todo successfully deleted"
#         }

#         return Response(data, status=status.HTTP_204_NO_CONTENT)



#* **GenericAPIView, mixin




class TodoList(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 




#* Concrete Views (mixin ile genericview birleşimi)

class TodoListCreate(ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializers

    # def perform_create(self, serializer):  #create islemin yapan userı alıyor
    #     serializer.save(user=self.request.user)


class TodoGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializers
    lookup_field = "id"  



#* ViewSet 

class TodoMVS(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializers

    # router ile action decaratörünü kullanarak kaçtane done todo olduğunu veriyor
    @action(methods=["GET"], detail=False)
    def todo_count(self, request):
        todo_count = Todo.objects.filter(done=False).count()
    
        count = {
        'undo-todos': todo_count
    }
        return Response(count)




class CategoryListCreate(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class= CategorySerializers



class CategoryGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    lookup_field = "id" 
