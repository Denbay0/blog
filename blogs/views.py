from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BlogPostForm
from .models import BlogPost

def index(request):
    return render(request, "blogs/index.html", {"posts": BlogPost.objects.select_related("owner")})

def detail(request, pk):
    return render(request, "blogs/detail.html", {"post": get_object_or_404(BlogPost.objects.select_related("owner"), pk=pk)})

@login_required
def create(request):
    form = BlogPostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.owner = request.user
        post.save()
        return redirect("blogs:detail", pk=post.pk)
    return render(request, "blogs/form.html", {"form": form, "title": "Новая публикация"})

@login_required
def edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, owner=request.user)
    form = BlogPostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blogs:detail", pk=post.pk)
    return render(request, "blogs/form.html", {"form": form, "title": "Редактирование"})
