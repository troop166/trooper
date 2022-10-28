from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CalendarsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trooper.calendars"
    verbose_name = _("Calendars")
