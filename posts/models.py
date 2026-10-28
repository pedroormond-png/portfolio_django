from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField("titulo", max_length=200)
    content = models.TextField("conteudo HTML")
    published_at = models.DateTimeField("data da postagem", default=timezone.now)
    categories = models.ManyToManyField("Category", related_name="posts", blank=True, verbose_name="categorias")

    class Meta:
        ordering = ["-published_at", "-id"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="post")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolio_comments", verbose_name="autor")
    text = models.TextField("texto")
    created_at = models.DateTimeField("data do comentario", default=timezone.now)

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"

    def __str__(self):
        return f"{self.author} - {self.post}"


class Category(models.Model):
    name = models.CharField("nome", max_length=120, unique=True)
    description = models.TextField("descricao")

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name
