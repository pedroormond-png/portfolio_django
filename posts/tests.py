"""Testes funcionais para executar com `python manage.py test`."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Category, Comment, Post


class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user(username="autor", password="SenhaForte2026!", is_staff=True)
        cls.reader = User.objects.create_user(username="leitor", password="SenhaForte2026!")
        cls.cat = Category.objects.create(name="Mecanica", description="testes")
        cls.post = Post.objects.create(title="Post de teste", content="<p>Conteudo</p>", published_at=timezone.now())
        cls.post.categories.add(cls.cat)

    def test_list_and_detail(self):
        response = self.client.get(reverse("posts:post_list"))
        self.assertContains(response, "Post de teste")
        response = self.client.get(reverse("posts:post_detail", args=[self.post.pk]))
        self.assertContains(response, "<p>Conteudo</p>", html=True)
        self.assertContains(response, "Mecanica")

    def test_missing_post_and_category_are_404(self):
        self.assertEqual(self.client.get(reverse("posts:post_detail", args=[99999])).status_code, 404)
        self.assertEqual(self.client.get(reverse("posts:category_detail", args=[99999])).status_code, 404)

    def test_crud_restricted_to_staff(self):
        url = reverse("posts:post_create")
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(self.staff)
        response = self.client.post(url, {"title": "Novo post", "content": "<p>Novo</p>"})
        new_post = Post.objects.get(title="Novo post")
        self.assertRedirects(response, reverse("posts:post_detail", args=[new_post.pk]))
        response = self.client.post(reverse("posts:post_update", args=[new_post.pk]), {"title": "Atualizado", "content": "<p>Outro</p>"})
        self.assertRedirects(response, reverse("posts:post_detail", args=[new_post.pk]))
        response = self.client.get(reverse("posts:post_delete", args=[new_post.pk]))
        self.assertContains(response, "Confirmar exclusão")
        self.client.post(reverse("posts:post_delete", args=[new_post.pk]))
        self.assertFalse(Post.objects.filter(pk=new_post.pk).exists())

    def test_comments_newest_first_and_logged_user(self):
        Comment.objects.create(post=self.post, author=self.reader, text="primeiro")
        Comment.objects.create(post=self.post, author=self.reader, text="segundo")
        r = self.client.get(reverse("posts:post_detail", args=[self.post.pk]))
        self.assertLess(r.content.index(b"segundo"), r.content.index(b"primeiro"))
        url = reverse("posts:comment_create", args=[self.post.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.reader)
        r = self.client.post(url, {"text": "comentario de teste"})
        self.assertRedirects(r, reverse("posts:post_detail", args=[self.post.pk]))
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.reader, text="comentario de teste").exists())

    def test_category_uses_post_list_template(self):
        r = self.client.get(reverse("posts:category_detail", args=[self.cat.pk]))
        self.assertTemplateUsed(r, "posts/post_list.html")
        self.assertContains(r, "Post de teste")
