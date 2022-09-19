from django.db import models

# Create your models here.

class Path(models.Model):
    path_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.path_name




class Student(models.Model):
    path = models.ForeignKey(Path, related_name="students",  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    number = models.IntegerField(blank=True, null=True)
    register_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return f"{self.first_name}-{self.last_name}"   


       

