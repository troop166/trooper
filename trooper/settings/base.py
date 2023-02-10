"""
Django settings for Trooper.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""


from email.utils import getaddresses
from pathlib import Path

from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = BASE_DIR / "trooper"


# 12factor
# https://www.12factor.net
# https://django-environ.readthedocs.io/en/latest/

env = Env()
dot_env = BASE_DIR / ".env"
if dot_env.is_file():
    env.read_env(dot_env)


# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "colorfield",
    "django_htmx",
    "recurrence",
    "sorl.thumbnail",
    "widget_tweaks",
    # First Party
    "trooper.address_book",
    "trooper.assignments",
    "trooper.calendars",
    "trooper.core",
    "trooper.members",
    "trooper.website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # https://whitenoise.evans.io/en/latest/django.html#enable-whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # https://django-htmx.readthedocs.io/en/latest/middleware.html
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "trooper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "trooper.website.context_processors.website",
            ],
        },
    },
]

WSGI_APPLICATION = "trooper.wsgi.application"


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    "default": env.db(default="sqlite:///db.sqlite3"),
}
if env("DATABASE_OPTIONS", default=None):
    DATABASES["default"]["OPTIONS"] = env.dict("DATABASE_OPTIONS", default=None)

# Cache
# https://docs.djangoproject.com/en/stable/ref/setting/#caches

CACHES = {
    "default": env.cache(default="locmemcache://"),
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

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


# Password hashing
# https://docs/djangoproject.com/en/stable/topics/auth/passwords/#using-argon2-with-django

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Custom user model
# https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "members.Member"
LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "home_page"
LOGOUT_REDIRECT_URL = "home_page"


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")

LOCALE_PATHS = [APP_DIR / "locale"]

TIME_ZONE = env("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/


STATIC_HOST = env("DJANGO_STATIC_HOST", default="")
STATIC_ROOT = env("DJANGO_STATIC_ROOT", default=BASE_DIR / "static_files")
STATIC_URL = f"{STATIC_HOST}/static/"
STATICFILES_DIRS = [APP_DIR / "static"]

# Include node packages if folder exists
NODE_MODULES = BASE_DIR / "node_modules"
if NODE_MODULES.is_dir():
    STATICFILES_DIRS.append(NODE_MODULES)

# https://whitenoise.evans.io/en/latest/django.html#add-compression-and-caching-support
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Media files (user uploaded)
# https://docs.djangoproject.com/en/stable/topics/files/

MEDIA_ROOT = env("DJANGO_MEDIA_ROOT", default=BASE_DIR / "media_files")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
# https://docs.djangoproject.com/en/stable/howto/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {"format": "[%(name)s] %(levelname)s: %(message)s"},
        "full": {"format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s"},
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": [],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Email
# https://docs.djangoproject.com/en/stable/topics/email/

EMAIL_CONFIG = env.email_url("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)
ADMINS = getaddresses([env("DJANGO_ADMINS", default="")])
MANAGERS = getaddresses([env("DJANGO_MANAGERS", default="")])
DEFAULT_FROM_EMAIL = env("DJANGO_FROM_EMAIL", default="webmaster@localhost")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default="root@localhost")


# Django-phonenumber-field
# https://github.com/stefanfoulis/django-phonenumber-field#settings

PHONENUMBER_DEFAULT_REGION = env("PHONENUMBER_DEFAULT_REGION", default="US")


# sorl-thumbnail
# https://sorl-thumbnail.readthedocs.io/en/latest/reference/settings.html

THUMBNAIL_ALTERNATIVE_RESOLUTIONS = [2]
THUMBNAIL_PRESERVE_FORMAT = True
