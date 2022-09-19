from rest_framework import serializers
from .models import Student, Path
from django.utils.timezone import now



# class StudentSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=50)
#     last_name= serializers.CharField(max_length=50)
#     number = serializers.IntegerField()
    
#     def create(self, validated_data):
#         return Student.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.number = validated_data.get('number', instance.number)
#         instance.save()
#         return instance



class StudentSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    # serializers method field ile modelde olmayan bir field ekleyebiliyoruz.
    class Meta:
        model = Student
        # fields = [ "id", "first_name", "last_name", "number"]
        # fields = "__all__"
        exclude = ["id"]
    
    #field level validate
    def validate_first_name(self, value):
        if value.lower() == "rafe":
            raise serializers.ValidationError("rafe can not be our student!")
        return value


    def validate_number(self, value):
        if value >2000:
            raise serializers.ValidationError("Student number can not be greather than 20001")
        return value 


    def get_days_since_joined(self, obj):
        return (now() - obj.register_date).days   


class PathSerializer(serializers.ModelSerializer):

    # students = StudentSerializer(many=True) # nesned olarak tüm veri geliyor 

    # students = serializers.StringRelatedField(many=True) # modeldeki str ile tanımlı olan geliyor

    students = serializers.PrimaryKeyRelatedField(read_only=True, many=True) # id ile gösterilir
    class Meta:
        model = Path
        fields = '__all__'                         