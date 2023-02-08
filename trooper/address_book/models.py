from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.translation import gettext as _

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


class AddressBookQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def subscribed(self):
        return self.filter(is_subscribed=True)


class Address(models.Model):
    class Label(models.TextChoices):
        HOME = "H", _("Home")
        SCHOOL = "S", _("School")
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
        _("published in the directory"),
        default=True,
        help_text=_("Allow other members to see this address in the Troop directory."),
    )

    # Mandatory fields for generic relation
    # https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()

    objects = AddressBookQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.as_single_line

    def get_absolute_url(self):
        return reverse(
            "address_book:address_form",
            kwargs={"pk": self.pk, "username": self.content_object.username},
        )

    @cached_property
    def as_single_line(self):
        fields = [self.street, self.street2, self.city, self.state, self.zipcode]
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
                self.zipcode,
            )
        else:
            return format_html(
                "{}<br> {}, {} {}", self.street, self.city, self.state, self.zipcode
            )


class Email(models.Model):
    class Label(models.TextChoices):
        HOME = "H", _("Home")
        SCHOOL = "S", _("School")
        WORK = "W", _("Work")
        OTHER = "O", _("Other")

    label = models.CharField(
        _("label"), max_length=1, choices=Label.choices, blank=True
    )
    address = models.EmailField(_("email address"), unique=True)
    is_published = models.BooleanField(
        _("published in directory"),
        default=True,
        help_text=_("Allow others to see this address in the member directory."),
    )
    is_subscribed = models.BooleanField(
        _("subscribed to mailing lists"),
        default=True,
        help_text=_("Receive periodic email communications at this address."),
    )

    # Mandatory fields for generic relation
    # https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()

    objects = AddressBookQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = _("Email Address")
        verbose_name_plural = _("Email Addresses")

    def __str__(self):
        return self.address


class Phone(models.Model):
    class Label(models.TextChoices):
        HOME = "H", _("Home")
        MOBILE = "M", _("Mobile")
        SCHOOL = "S", _("School")
        WORK = "W", _("Work")
        OTHER = "O", _("Other")

    label = models.CharField(
        _("label"), max_length=1, choices=Label.choices, blank=True
    )
    number = PhoneNumberField(_("phone number"))
    is_published = models.BooleanField(
        _("published in directory"),
        default=True,
        help_text=_("Allow other members to see this number in the Troop directory."),
    )

    # Mandatory fields for generic relation
    # https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()

    objects = AddressBookQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

    def __str__(self):
        return self.number.as_national
