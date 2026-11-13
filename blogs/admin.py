from django.contrib import admin
from .models import BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "date_added", "updated_at")
    list_filter = ("date_added", "owner")
    search_fields = ("title", "text", "owner__username")
    date_hierarchy = "date_added"
