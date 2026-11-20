from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "DJANGO_SECRET_KEY", default="django-insecure-local-development-key"
)

DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1"
).split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "projects",
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

ROOT_URLCONF = "team_finder.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates_var2"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "team_finder.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST", default="localhost"),
        "PORT": config("POSTGRES_PORT", cast=int),
    }
}

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "users:login"

PASSWORD_VALIDATION = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = []
if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": f"{PASSWORD_VALIDATION}.UserAttributeSimilarityValidator"},
        {"NAME": f"{PASSWORD_VALIDATION}.MinimumLengthValidator"},
        {"NAME": f"{PASSWORD_VALIDATION}.CommonPasswordValidator"},
        {"NAME": f"{PASSWORD_VALIDATION}.NumericPasswordValidator"},
    ]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
