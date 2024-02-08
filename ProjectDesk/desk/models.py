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

class Comment(models.Model):
    commentPost = models.ForeignKey(Post,on_delete=models.CASCADE,verbose_name='комментарий')
    commentUser = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='автор')
    text = models.TextField(max_length=500,verbose_name='текст')
    status = models.BooleanField(default=False,verbose_name='статус')
    def __str__(self):
        return f'{self.commentUser}:{self.text} [:20] + ...'

    def get_absolut_url(self):
        return reverse('news_id',kwargs={'pk':self.commentPost_id})
    class Meta:
        verbose_name = 'комментарий'
        ordering = ['id']

class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)#связь многи ко многим с пост
    category = models.ForeignKey(Category,on_delete=models.CASCADE)