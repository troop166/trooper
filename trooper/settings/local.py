import importlib.util

from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-c#p2tsup@!p3yjxxoi9dbk)xb_iq1e5*_x&n)d$!*hc8@wuh*f",
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Logging
# https://docs.djangoproject.com/en/stable/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}


# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/

# https://docs.python.org/3/library/importlib.html#checking-if-a-module-can-be-imported
if importlib.util.find_spec("debug_toolbar") is not None:
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )


# Sorl-thumbnail
# https://sorl-thumbnail.readthedocs.io/en/latest/reference/settings.html

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_DUMMY = DEBUG


# Whitenoise
# https://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS


# Django Extensions
# https://django-extensions.readthedocs.io/en/latest/index.html

INSTALLED_APPS += ["django_extensions"]
