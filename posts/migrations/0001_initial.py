from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="titulo")),
                ("content", models.TextField(verbose_name="conteudo HTML")),
                ("published_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="data da postagem")),
            ],
            options={"verbose_name": "post", "verbose_name_plural": "posts", "ordering": ["-published_at", "-id"]},
        ),
    ]
