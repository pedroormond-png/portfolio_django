from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("posts", "0002_comment")]
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="nome")),
                ("description", models.TextField(verbose_name="descricao")),
            ],
            options={"verbose_name": "categoria", "verbose_name_plural": "categorias", "ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="post",
            name="categories",
            field=models.ManyToManyField(blank=True, related_name="posts", to="posts.category", verbose_name="categorias"),
        ),
    ]
