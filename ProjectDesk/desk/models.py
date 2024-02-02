from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=64)

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь один ко многим с автором
    category = models.ManyToManyField(Category,through='PostCategory')  # связь с доп моделью посткатегори и категори
    header = models.CharField(max_length=100, unique=True, )  # заголовок статьи
    text = models.TextField()  # текст
    rating = models.IntegerField(default=0)  # рейтинг статьи
    labels = {}

class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)#связь многи ко многим с пост
    category = models.ForeignKey(Category,on_delete=models.CASCADE)