from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Tag(models.Model):
    name = models.CharField(max_length=200)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, name = 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, name='comments')
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()