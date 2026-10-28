"""Versao 2: views funcionais com ModelForm e validacao integrada."""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Post


def post_list(request):
    return render(request, "posts/post_list.html", {"posts": Post.objects.all()})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/post_detail.html", {"post": post})


@staff_member_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        return redirect("posts:post_detail", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form})


@staff_member_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        return redirect("posts:post_detail", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "object": post})


@staff_member_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("posts:post_list")
    return render(request, "posts/post_confirm_delete.html", {"object": post})
