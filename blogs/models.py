from django.contrib.auth.models import User
from django.db import models

class BlogPost(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return self.title
