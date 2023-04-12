from django.db import models
from django.db.models.functions import Lower
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.translation import gettext as _

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    street = models.CharField(_("street"), max_length=150)
    street2 = models.CharField(
        _("street 2"),
        max_length=150,
        blank=True,
        help_text=_("e.g. Apartment, Suite, Box Number"),
    )
    city = models.CharField(_("city"), max_length=50)
    state = USStateField(_("state"))
    zip_code = USZipCodeField(_("ZIP code"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.as_single_line

    @cached_property
    def as_single_line(self):
        fields = [self.street, self.street2, self.city, self.state, self.zip_code]
        return ", ".join(field.strip() for field in fields if field)

    @cached_property
    def as_multiline(self):
        if self.street2:
            return format_html(
                "{}<br> {}<br> {}, {} {}",
                self.street,
                self.street2,
                self.city,
                self.state,
                self.zip_code,
            )
        else:
            return format_html(
                "{}<br> {}, {} {}",
                self.street,
                self.city,
                self.state,
                self.zip_code,
            )


class EmailAddressManager(models.Manager):
    def get_by_natural_key(self, address):
        return self.get(address__iexact=address)


class EmailAddress(models.Model):
    address = models.EmailField(_("email address"), unique=True)

    objects = EmailAddressManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("address"), name="unique_email_address"),
        ]
        verbose_name = _("Email Address")
        verbose_name_plural = _("Email Addresses")

    def __str__(self):
        return self.address

    def natural_key(self):
        return (self.address.lower(),)


class PhoneNumberManager(models.Manager):
    def get_by_natural_key(self, number):
        return self.get(number=number)


class PhoneNumber(models.Model):
    number = PhoneNumberField(_("phone number"), unique=True)

    objects = PhoneNumberManager()

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

    def __str__(self):
        return self.number.as_national

    def natural_key(self):
        return (self.number.as_e164,)


class Location(models.Model):
    name = models.CharField(_("name"), max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.name
