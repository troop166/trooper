from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.utils.translation import gettext as _

from trooper.address_book.forms import AddressForm
from trooper.address_book.models import Address, Email, Phone


class AddressInline(GenericStackedInline):
    model = Address
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "label",
                    "street",
                    "street2",
                    ("city", "state", "zipcode"),
                    "is_published",
                )
            },
        ),
    )
    form = AddressForm


class EmailInline(GenericTabularInline):
    model = Email
    extra = 0
    fields = ("label", "address", "is_published", "is_subscribed")


class PhoneInline(GenericTabularInline):
    model = Phone
    extra = 0
    fields = ("label", "number", "is_published")
