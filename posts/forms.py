from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Form do Django para criacao e edicao de posts."""

    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 12})}
        labels = {"title": "Título", "content": "Conteúdo HTML"}


from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Comentário"}
        widgets = {"text": forms.Textarea(attrs={"rows": 5})}
