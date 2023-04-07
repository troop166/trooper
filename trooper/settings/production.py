from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=60 * 60 * 24)
SECURE_PROXY_SSL_HEADER = env.tuple("SECURE_PROXY_SSL_HEADER", default=None)
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)

# Logging
# LOGGING["handlers"]["syslog"] = {
#     "formatter": "full",
#     "level": "DEBUG",
#     "class": "logging.handlers.SysLogHandler",
#     "address": "/dev/log",
#     "facility": "local4",
# }
# LOGGING["loggers"]["django.request"]["handlers"].append("syslog")


# Sentry support
# https://docs.sentry.io/platforms/python/guides/django/
if "SENTRY_DSN" in env and not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default=""),
        integrations=[DjangoIntegration()],
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.1),
        send_default_pii=env.bool("SENTRY_SEND_DEFAULT_PII", default=True),
    )
