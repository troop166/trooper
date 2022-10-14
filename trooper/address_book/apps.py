from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AddressBookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trooper.address_book"
    verbose_name = _("Address Book")
