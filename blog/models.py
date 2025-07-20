from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    image=models.ImageField(upload_to="blog/",default="blog/default.jpg")
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE,null=True)
    #tag
    category=models.ManyToManyField(Category)
    counted_views=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    published_date=models.DateTimeField(null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['status']

    
    def __str__(self):
        return self.title