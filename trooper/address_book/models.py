from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    class Label(models.TextChoices):
        HOME = "H", _("Home")
        WORK = "W", _("Work")
        PO_BOX = "B", _("P.O. Box")
        OTHER = "O", _("Other")

    label = models.CharField(
        _("label"), max_length=1, choices=Label.choices, blank=True
    )
    street = models.CharField(_("street"), max_length=150)
    street2 = models.CharField(
        _("street 2"),
        max_length=150,
        blank=True,
        help_text=_("e.g. Apartment, Suite, Box Number"),
    )
    city = models.CharField(_("city"), max_length=50)
    state = USStateField(_("state"))
    zipcode = USZipCodeField(_("ZIP code"))

    is_published = models.BooleanField(
        _("publish in the directory"),
        default=True,
        help_text=_("Allow other members to see this address in the Troop directory."),
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    @cached_property
    def as_single_line(self):
        fields = [self.street, self.street2, self.city, self.state, self.zipcode]
        return ", ".join(field.strip() for field in fields if field)


class Email(models.Model):
    class Label(models.TextChoices):
        HOME = "H", _("Home")
        WORK = "W", _("Work")
        OTHER = "O", _("Other")

    label = models.CharField(
        _("label"), max_length=1, choices=Label.choices, blank=True
    )
    address = models.EmailField(_("email address"), unique=True)

    is_published = models.BooleanField(
        _("publish in directory"),
        default=True,
        help_text=_("Allow other members to see this address in the Troop directory."),
    )
    is_subscribed = models.BooleanField(
        _("subscribed to mailing lists"),
        default=True,
        help_text=_("Receive Troop communications at this email address. "),
    )

    class Meta:
        verbose_name = _("Email Address")
        verbose_name_plural = _("Email Addresses")

    def __str__(self):
        return self.address


class Phone(models.Model):
    class Label(models.TextChoices):
        HOME = "H", _("Home")
        MOBILE = "M", _("Mobile")
        WORK = "W", _("Work")
        OTHER = "O", _("Other")

    label = models.CharField(
        _("label"), max_length=1, choices=Label.choices, blank=True
    )
    number = PhoneNumberField(_("phone number"))

    is_published = models.BooleanField(
        _("publish in directory"),
        default=True,
        help_text=_("Allow other members to see this number in the Troop directory."),
    )

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

    def __str__(self):
        return self.number.as_national
