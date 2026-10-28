"""Preenche o portfolio com exatamente os dados minimos pedidos na entrega."""
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from posts.models import Category, Comment, Post


POSTS = [
    (
        "Análise de Concentração de Tensões por Elementos Finitos",
        "<p>Estudo da distribuição de tensões em componentes mecânicos, "
        "com atenção às regiões de descontinuidade geométrica.</p>"
        "<h3>Objetivo</h3><p>Investigar a concentração de tensões com um "
        "modelo de elementos finitos e discutir os efeitos da geometria.</p>"
        "<h3>Etapas</h3><p>Definição do componente, condições de contorno, "
        "análise numérica e interpretação dos resultados.</p>",
        ("Mecânica", "Simulação"),
    ),
    (
        "Controle Sequencial de uma Célula Eletropneumática",
        "<p>Projeto de uma lógica de acionamento sequencial "
        "para uma célula eletropneumática.</p>"
        "<h3>Objetivo</h3><p>Organizar sinais de sensores e atuadores "
        "para executar uma sequência de operação.</p>"
        "<h3>Etapas</h3><p>Mapeamento de entradas e saídas, "
        "descrição da sequência, testes e análise do funcionamento.</p>",
        ("Automação", "Simulação"),
    ),
    (
        "Determinação Experimental de Vazão em Tubulação",
        "<p>Atividade experimental para observar o escoamento de fluidos "
        "e estimar a vazão em uma tubulação.</p>"
        "<h3>Objetivo</h3><p>Relacionar medições experimentais "
        "aos princípios de mecânica dos fluidos.</p>"
        "<h3>Etapas</h3><p>Preparação da bancada, coleta de medidas, "
        "cálculos e comparação dos resultados.</p>",
        ("Mecânica",),
    ),
]

COMMENTS = [
    (0, "comentador_demo", "Excelente apresentação do método de elementos finitos!", 1),
    (0, "leitor_demo", "A discussão sobre as condições de contorno ficou clara.", 2),
    (0, "comentador_demo", "Gostei da organização das etapas de simulação.", 3),
    (1, "leitor_demo", "O sequenciamento de atuadores foi bem descrito.", 1),
    (1, "comentador_demo", "Projeto interessante para aplicações de automação.", 2),
]


class Command(BaseCommand):
    help = "Cria 3 posts, 3 categorias e 5 comentarios sem duplicar registros existentes."

    def add_arguments(self, parser):
        parser.add_argument("--production", action="store_true", help="Nao criar senhas de teste conhecidas.")

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        demo_users = {}
        for username in ("comentador_demo", "leitor_demo"):
            user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.invalid"})
            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
            demo_users[username] = user

        # Admin configurado somente pelo proprietario com env vars privadas.
        admin_name = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        admin_password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        if admin_name and admin_password and not User.objects.filter(username=admin_name).exists():
            User.objects.create_superuser(
                username=admin_name,
                email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
                password=admin_password,
            )

        cat_descriptions = {
            "Mecânica": "Projetos de análise estrutural e mecânica dos fluidos.",
            "Simulação": "Aplicações de modelos computacionais e análise de sistemas.",
            "Automação": "Controle de processos e sistemas eletropneumáticos.",
        }
        categories = {}
        for name, description in cat_descriptions.items():
            categories[name], _ = Category.objects.get_or_create(name=name, defaults={"description": description})

        posts = []
        for index, (title, content, category_names) in enumerate(POSTS):
            post, _ = Post.objects.get_or_create(
                title=title,
                defaults={"content": content, "published_at": timezone.now() - timedelta(days=index + 1)},
            )
            post.categories.set([categories[name] for name in category_names])
            posts.append(post)

        for post_index, username, text, minutes_ago in COMMENTS:
            Comment.objects.get_or_create(
                post=posts[post_index], author=demo_users[username], text=text,
                defaults={"created_at": timezone.now() - timedelta(minutes=minutes_ago)},
            )
        self.stdout.write(self.style.SUCCESS("Dados de demonstracao prontos: 3 posts, 3 categorias, 5 comentarios."))
