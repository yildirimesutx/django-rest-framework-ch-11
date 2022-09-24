from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
       return self.name 


class Todo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categorys")
    task = models.CharField(max_length=50)
    description = models.TextField()

    TITLE = (
      ("H", "High"),
      ("M", "Medium"),
      ("L", "Low")

    )

    priority = models.CharField(max_length=50, choices=TITLE, default="L")
    done = models.BooleanField()
    updateDate = models.DateTimeField(auto_now=True)
    createDate = models.DateTimeField(auto_now_add=True )


    def __str__(self):
        return self.task
