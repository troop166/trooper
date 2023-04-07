from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OutingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trooper.outings"
    verbose_name = _("Outings")
