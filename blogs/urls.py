from django.urls import path
from . import views
app_name = "blogs"
urlpatterns = [path("", views.index, name="index"), path("posts/new/", views.create, name="create"), path("posts/<int:pk>/", views.detail, name="detail"), path("posts/<int:pk>/edit/", views.edit, name="edit")]
