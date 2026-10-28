from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField("titulo", max_length=200)
    content = models.TextField("conteudo HTML")
    published_at = models.DateTimeField("data da postagem", default=timezone.now)

    class Meta:
        ordering = ["-published_at", "-id"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title
