# Portfólio de Engenharia - Django

Segunda entrega de laboratório de PMR3304. Site dinâmico usando **somente o Django** (sem bibliotecas de extensões), contendo CRUD de posts, comentários por usuários autenticados, categorias e SQL. Os três projetos são baseados nos títulos da primeira entrega de portfólio Hugo.

O relatório e o banco preenchido `db.sqlite3` são fornecidos **separadamente** do repositório, conforme enunciado. O arquivo `.gitignore` evita que o banco seja publicado.

## Estrutura e evidências do Git

- 3 commits separados com as 3 implementações de `posts/views.py`.
- Branch `comments`, integrada ao principal por merge.
- Branch `categories`, criada após o merge anterior, também integrada.
- Capturas de tela e SQL em `docs/`.

## Execução local (Windows: PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. O banco fornecido em separado já contém dados. Coloque-o ao lado de `manage.py` **antes** de executar `migrate` se quiser utilizar os dados prontos.

Para gerar dados em um banco novo, depois de `migrate`, execute:

```powershell
python manage.py seed_demo
python manage.py createsuperuser
```

Criar usuários comuns pelo `/admin/`. Apenas usuários autenticados podem comentar; apenas usuários com `is_staff=True` podem criar, editar ou excluir posts. A página de login fica em `/accounts/login/`.

## Testes

```powershell
python manage.py test
python manage.py check
```

## Render

Incluído `render.yaml` (Blueprint), com execução `gunicorn config.wsgi:application`. A conta de GitHub/Render e a primeira publicação precisam ser autorizadas pelo proprietário. Recomendado configurar em Render as variáveis `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD` e `DJANGO_SUPERUSER_EMAIL` para criar conta administradora durante a inicialização.

**Persistência:** no plano gratuito do Render, o sistema de arquivos é efêmero; alterações feitas no banco SQLite remoto podem ser perdidas ao reiniciar/reimplantar. Para uma aplicação permanente, use banco PostgreSQL gerenciado ou disco persistente em plano compatível. Para esta entrega, o SQLite local enviado ao Moodle é a referência para as consultas SQL.

## Dados de exemplo

Três posts, três categorias e cinco comentários distribuídos em dois posts (o terceiro post não tem comentários). Cada post possui ao menos uma categoria; dois posts estão associados a múltiplas categorias. SQL em `docs/sql/consultas.sql`.
