from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Post

def index(request):
    return render(request, "posts/index.html", {"posts": Post.objects.select_related("author")})

def detail(request, pk):
    return render(request, "posts/detail.html", {"post": get_object_or_404(Post.objects.select_related("author"), pk=pk)})

@login_required
def create(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:detail", pk=post.pk)
    return render(request, "posts/form.html", {"form": form, "title": "Новая публикация"})

@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("posts:detail", pk=post.pk)
    return render(request, "posts/form.html", {"form": form, "title": "Редактирование"})
