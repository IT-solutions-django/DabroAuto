from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = '=$&(7o&+rgd9ly+x2avwrggb7lmtw-cuapm(@=q0&p2tw6whn&'

DEBUG = False

ALLOWED_HOSTS = ["194.87.56.114"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps
    "apps.car",
    "apps.review",
    "apps.service_info",
    "apps.image",
    "apps.clip",
    "apps.catalog",
    "apps.telegram_sender",
    "apps.commission",
    # Pages
    "pages.home",
    "pages.catalog_page",
    "pages.car_card",
    # Prom Apps
    "custom_commands",
    "tasks",
    "pages",
    "tags",
    "apps.delivery"
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("CACHE_LOCATION_URL"),
    }
}

LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Barnaul"

USE_I18N = True

USE_TZ = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
API_KEY_2GIS = os.getenv("API_KEY_2GIS")

CLIPS_PATH = os.path.join(BASE_DIR, "media", "clips")

PROXY_URL = os.getenv("PROXY_URL")

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = "Asia/Barnaul"

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")

SERVER_IP = "194.87.56.114"

CACHE_TIMEOUT = 60 * 30

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

APPEND_SLASH = False

# Email configuration
DEFAULT_FROM_EMAIL = 'Matvey-Django@yandex.ru'
CONTACT_EMAIL = 'matvejvarlamov495@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'Matvey-Django@yandex.ru'
EMAIL_HOST_PASSWORD = 'qlmdfckrcruclgju'
