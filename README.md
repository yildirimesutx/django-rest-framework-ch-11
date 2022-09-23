# Django REST Framework

Bu projedeki amacımız Django Rest Framework'u, olusturacagımız 5 app ile ozetlemek. 

```
app_1 => serializers, relation field
app_2 => FBV
app_3 => CBV
app_4 => Pagination, filter, search
 




```





**app_1 (Serializers)**

- Bu app de views.py dosyasını hazır aldık, bu app de sadece aşağıda belirtilen hususlara değinilmiştir.


- Serializers
     - Serializer class
     - ModelSerializer class
- Custom Validations
- Additional Features
- Relational fields
     - StringRelatedField
     - PrimaryKeyRelatedField
- Serializer Fields
     - read_only
     - write_only
- Nested Serializer



<img src="api.png">
<img src="serializers.png">

İlgili app içinde serializers.py dosyası oluşturun.

serializers.Serializer: ile models.py da tanımlanan tüm fields tekrar tanımlıyoruz.

Bu yöntemde CRUD işlemleri için ayrıca class içinde func ları tanımlamak gerekli.

tanımlamada models.py daki attributlerin kullanılması gerekiyor



serializers.py 

```

from rest_framework import serializers




class StudentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name= serializers.CharField(max_length=50)
    number = serializers.IntegerField()

# yukarıdaki class bize api görüntülemek için yeterli, fakat crud islemleri icin  asagidaki yapilara ihtiyaci var.


    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance


PUT : tamamının update edilmesi
PATCH : yalnızca birkaç alanın update edilmesi


```

**ModelSerializer**

ModelSerializers da crud islemleri icin ek bir isleme gerek yok

```
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = [ "id", "first_name", "last_name", "number"]
        # fields = "__all__"
        exclude = ["id"]
```




**Custom Validations**

- Field-level validation
```
def validate_first_name(self, value):
        if value.lower() == "rafe":
            raise serializers.ValidationError("rafe can not be our student!")
        return value  
```



- Object-level validation 

https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation


- SerializersMethod Field


```
class StudentSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    # serializers method field ile modelde olmayan bir field ekleyebiliyoruz.
    class Meta:
        model = Student
        # fields = [ "id", "first_name", "last_name", "number"]
        # fields = "__all__"
        exclude = ["id"]



    def get_days_since_joined(self, obj):
        return (now() - obj.register_date).days  


# serializers method field ile modelde olmayan bir field ekleyebiliyoruz.        
```


**Relational fields**

https://www.django-rest-framework.org/api-guide/relations/#nested-relationships



```
*Nested Serializer
öğrenci tablomuza ayrıca ForeignKey ile path tablomuzu bağladık

path = models.ForeignKey(Path,related_name='students', on_delete=models.CASCADE)

ForeignKey tanımlarken related_name='students' isimlendirdiğimiz atribut ile geliyor ÖNEMLİ

example :her bir path altında tanımlanan öğrenciler gözüksün 




class PathSerializer(serializers.ModelSerializer):

    # students = StudentSerializer(many=True) # nesned olarak tüm veri geliyor 

    # students = serializers.StringRelatedField(many=True) # modeldeki str ile tanımlı olan geliyor

    students = serializers.PrimaryKeyRelatedField(read_only=True, many=True) # id ile gösterilir
    class Meta:
        model = Path
        fields = '__all__' 
```


**app_2 FBV restful**



 - bu app de views.py da POST GET DELETE UPDATE iislemleri icin func yazarak tanımladık, postmande denem yaptık


```
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

```


**app_3 (CBV RESTFUL)**


- class APIView den inherit ederek kullanıyoruz




```
from django.shortcuts import render, get_object_or_404

from .models import Todo
from .serializers import TodoSerializers

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
```
- yazılan apide herbir veri için url oluşturma
```

serialiazers.py



class TodoSerializer(serializers.ModelSerializer):
    todo_detail = serializers.HyperlinkedIdentityField(view_name="todo-detail")
   
    buradaki view_name = model adı-detail (detail doc geliyor)


    class Meta:
        model= Todo
        fields = ("id", "task","description","priority", "done", "todo_detail" ,  "updateDate", "createdDate" )



```


**app_4 Pagination, filter, search**

-Global ve local ayarlar yapabiliyoruz.


- Global olarak  asagidaki kodu settings.py yazıyoruz. 200 adet gelen veriyi 10 sayfaya bölüyor. Global tüm modelleri etkiler 

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```


- local


```
pagination.py 

from rest_framework.pagination import PageNumberPagination


# PageNumberPagination classını inherit ediyoruz ve yeni class farklı isimlendirebiliriz
# page_size bu inherit edilen class in attributi 
class SmallPageNumberPagination(PageNumberPagination):
    page_size = 8


views.py =>

ilgili modelde çağırdık,

class StudentMVS(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = SmallPageNumberPagination

```


- Limit Offset- global

- limit offet için settings.py


```

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}



http://127.0.0.1:8000/psf/api/?limit=10  urlde sorguluyoruz, ilk 10 kayıdı getiriyor


http://127.0.0.1:8000/psf/api/?limit=10&offset=15  ilk 15 den sonra 10 kayıdı getir
```



- limit-offset local

```
pagination.py

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3   

class StudentMVS(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # pagination_class = SmallPageNumberPagination
    pagination_class = MyLimitOffsetPagination


```


**app_5 Permission and Authentication**



- permission kullanıclara verilen yetki dahilinde belirli işlemlerin yapılabilmesini sağlıyor, örnek olarak, kayıtlı bir user listeleme yapabilsin, admin ise post edebilsin gibi, 

- https://www.django-rest-framework.org/api-guide/permissions/


- localde uygulama;

     ``` 
     views.py =>
      
    from rest_framework.permissions import IsAuthenticated # ilgili permission import ettik 


    class StudentList(generics.ListCreateAPIView):
        serializer_class = StudentSerializer
        queryset = Student.objects.all()
        permission_classes = [IsAuthenticated]
        (#burada cagirdik)



     
     ```

- BasicAuthetication kullanarak test ettik 

```
     settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
       
    ]
}
```