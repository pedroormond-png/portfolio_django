"""Configuracoes do portfolio de engenharia (Django puro, sem extensoes)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# O valor de desenvolvimento nao deve ser usado em ambiente de producao.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "desenvolvimento-apenas-trocar-em-producao-2026"
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1" if "RENDER" not in os.environ else "0") == "1"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
ALLOWED_HOSTS += [s.strip() for s in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if s.strip()]
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

CSRF_TRUSTED_ORIGINS = [
    s.strip() for s in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if s.strip()
]
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append("https://" + render_hostname)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "posts.apps.PostsConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Banco de dados SQLite local; nao inclui django-extensions ou outras extensoes.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.environ.get("DJANGO_DB_PATH", str(BASE_DIR / "db.sqlite3"))}}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "posts:post_list"
LOGOUT_REDIRECT_URL = "posts:post_list"

# Todo o CSS necessario esta dentro do template base, dispensando middleware de terceiros.
