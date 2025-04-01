"""
Django settings for kelvin project.

Generated by 'django-admin startproject' using Django 3.0b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

import dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from an .env file
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

KELVIN_ROOT_HOST = os.getenv("KELVIN__HOST_URL")

PUBLIC_URL = f"https://{KELVIN_ROOT_HOST}"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "***REMOVED***"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "app", KELVIN_ROOT_HOST]

CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1",
    "https://localhost",
    "https://app",
    f"https://{KELVIN_ROOT_HOST}",
]

# Application definition

INSTALLED_APPS = [
    "web.apps.WebConfig",
    "api.apps.ApiConfig",
    "survey.apps.SurveyConfig",
    "common.apps.CommonConfig",
    "quiz.apps.QuizConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "django_rq",
    # Used for configuring cron-like jobs
    # from django-tasks-scheduler
    "scheduler",
    "django_cas_ng",
    "notifications",
    "webpush",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "api.middleware.TokenAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_cas_ng.middleware.CASMiddleware",
]

ROOT_URLCONF = "kelvin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "web.views.common.template_context",
            ],
        },
    },
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "kelvin.wsgi.application"

DJANGO_NOTIFICATIONS_CONFIG = {"USE_JSONFIELD": True}

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Default type for primary keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DATABASE__HOST", "127.0.0.1"),
        "PORT": os.getenv("DATABASE__PORT", 5432),
        "NAME": os.getenv("DATABASE__DB"),
        "USER": os.getenv("DATABASE__USERNAME"),
        "PASSWORD": os.getenv("DATABASE__PASSWORD"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Prague"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "kelvin.storage.GzipStaticFilesStorage",
    },
}

INTERNAL_IPS = ("127.0.0.1",)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "api.backends.TokenBackend",
    "django_cas_ng.backends.CASBackend",
]

# This should be in sync with client_max_body_size from deploy/nginx.conf
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024

LOGIN_REDIRECT_URL = "/"

CAS_ENABLE = False
CAS_SERVER_URL = "https://www.sso.vsb.cz/"
CAS_CREATE_USER = False
CAS_FORCE_CHANGE_USERNAME_CASE = "upper"

REDIS_HOST = os.getenv("REDIS__HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS__PORT", 6379)
REDIS_CONNECTION = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONNECTION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# For django_rq
# "default" means that it reuses the Redis cache from CACHES["default"]
RQ_QUEUES = {
    "default": {
        "USE_REDIS_CACHE": "default",
    },
    "cuda": {
        "USE_REDIS_CACHE": "default",
    },
    "evaluator": {
        "USE_REDIS_CACHE": "default",
    },
}

# For django-tasks-scheduler
SCHEDULER_QUEUES = {"default": {"HOST": REDIS_HOST, "PORT": REDIS_PORT}}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] ({name}:{pathname}:{lineno}) {message}",
            "style": "{",
        },
        "http": {
            "format": "{asctime} [{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "console_http": {"class": "logging.StreamHandler", "formatter": "http"},
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        # Default logger for everything
        "": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
        },
        # Override format of default Django logs
        "django.server": {
            "handlers": ["console_http"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Disable logs from the serde and markdown crates, to avoid spam
        "serde": {"handlers": [], "level": "DEBUG", "propagate": False},
        "markdown": {"handlers": [], "level": "DEBUG", "propagate": False},
    },
}

MAX_INLINE_CONTENT_BYTES = 64565
MAX_INLINE_LINES = 2000

# DSN for a Sentry instance. If `None`, Sentry will not be included
SENTRY_URL = None

# Placeholder to ensure Kelvin runs locally without any configuration
# Prefer configuring Inbus credentials in local_settings.py imported at
# the end of this script
INBUS_CLIENT_ID = "placeholder"
INBUS_CLIENT_SECRET = "placeholder"


try:
    from .local_settings import *  # noqa: F403
except ModuleNotFoundError:
    pass
