from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    body = models.TextField("Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
