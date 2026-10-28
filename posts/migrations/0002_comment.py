from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(verbose_name="texto")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="data do comentario")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="portfolio_comments", to=settings.AUTH_USER_MODEL, verbose_name="autor")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="posts.post", verbose_name="post")),
            ],
            options={"verbose_name": "comentario", "verbose_name_plural": "comentarios", "ordering": ["-created_at", "-id"]},
        ),
    ]
