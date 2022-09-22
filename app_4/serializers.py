from rest_framework import serializers
from .models import Student, Path




class StudentSerializer(serializers.ModelSerializer):
   
    path = serializers.StringRelatedField()
    path_id = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ["id", "path", "path_id", "first_name", "last_name", "number"]
        # fields = '__all__'
        # exclude = ['number']


class PathSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Path
        fields = ["id", "path_name", "students"]