from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AssignmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trooper.assignments"
    verbose_name = _("Assignments")
