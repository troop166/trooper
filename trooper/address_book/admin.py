from django.contrib import admin

from trooper.address_book.forms import AddressForm, EmailForm, PhoneForm
from trooper.address_book.models import Address, EmailAddress, PhoneNumber


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "street",
                    "street2",
                    ("city", "state", "zip_code"),
                )
            },
        ),
    )


@admin.register(EmailAddress)
class EmailAdmin(admin.ModelAdmin):
    form = EmailForm


@admin.register(PhoneNumber)
class PhoneAdmin(admin.ModelAdmin):
    form = PhoneForm
