from rest_framework import serializers
from .models import Todo, Category
from django.utils.timezone import now



class TodoSerializers(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField() # modeldeki isim, default olarak id ile geliyor, eğer bunu Category serializers da releted_name ile kullanırsak nested olarak sergileriz.

    days = serializers.SerializerMethodField()  # 

    class Meta:
        model = Todo
        fields = "__all__"
    
    def get_days(self, obj):
        return (now() - obj.createDate).days  

    def validate_task(self, value):
        if value.lower() == "python":
            raise serializers.ValidationError("python can not be our task!")
        return value    


class CategorySerializers(serializers.ModelSerializer):
    categorys = TodoSerializers(many=True)
    # categorys = serializers.StringRelatedField(many=True) # modeldeki str ile tanımlı olan geliyor

    # categorys = serializers.PrimaryKeyRelatedField(read_only=True, many=True) 
    class Meta:
        model =Category
        fields ="__all__"