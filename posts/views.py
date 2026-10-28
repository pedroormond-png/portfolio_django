"""Versao 1: views funcionais, sem Django Forms e sem validacao de campos."""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post


def post_list(request):
    return render(request, "posts/post_list.html", {"posts": Post.objects.all()})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # 404 automatico para post inexistente
    return render(request, "posts/post_detail.html", {"post": post})


@staff_member_required
def post_create(request):
    if request.method == "POST":
        post = Post.objects.create(title=request.POST.get("title", ""), content=request.POST.get("content", ""))
        return redirect("posts:post_detail", pk=post.pk)
    return render(request, "posts/post_form.html")


@staff_member_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.title = request.POST.get("title", "")
        post.content = request.POST.get("content", "")
        post.save()
        return redirect("posts:post_detail", pk=post.pk)
    return render(request, "posts/post_form.html", {"object": post})


@staff_member_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("posts:post_list")
    return render(request, "posts/post_confirm_delete.html", {"object": post})
