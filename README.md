# Django REST Framework

Bu projedeki amacımız Django Rest Framework'u, olusturacagımız 5 app ile ozetlemek. 



**app_1 (Serializers)**

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








