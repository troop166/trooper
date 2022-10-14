from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trooper.website"
    verbose_name = _("Website")
