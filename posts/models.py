from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class SubPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='subposts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
