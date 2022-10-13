from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trooper.members"
    verbose_name = _("Members")
