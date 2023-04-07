from django.db import models
from django.utils.translation import gettext as _

from trooper.address_book.models import Address, Email, Phone

from .people import Member


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishedSubscribedQuerySet(PublishedQuerySet):
    def subscribed(self):
        return self.filter(is_subscribed=True)


class MemberAddress(models.Model):
    class Label(models.TextChoices):
        HOME = "HOME", _("Home")
        WORK = "WORK", _("Work")
        SCHOOL = "SCHOOL", _("School")
        PO_BOX = "POB", _("P.O. Box")

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    label = models.CharField(
        _("label"), max_length=6, choices=Label.choices, blank=True
    )
    is_published = models.BooleanField(
        _("published in directory"),
        default=True,
        help_text=_("Allow others to see this address in the member directory."),
    )

    objects = PublishedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return str(self.address)


class MemberEmail(models.Model):
    class Label(models.TextChoices):
        HOME = "HOME", _("Home")
        SCHOOL = "SCHOOL", _("School")
        WORK = "WORK", _("Work")

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    label = models.CharField(
        _("label"), max_length=6, choices=Label.choices, blank=True
    )
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

    objects = PublishedSubscribedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Email Address")
        verbose_name_plural = _("Email Addresses")

    def __str__(self):
        return str(self.email)


class MemberPhone(models.Model):
    class Label(models.TextChoices):
        """A subset of phone types from RFC 2426."""

        HOME = "HOME", _("Home")
        MOBILE = "CELL", _("Mobile")
        FAX = "FAX", _("Fax")
        WORK = "WORK", _("Work")

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    label = models.CharField(
        _("label"), max_length=4, choices=Label.choices, blank=True
    )
    is_published = models.BooleanField(
        _("published in directory"),
        default=True,
        help_text=_("Allow other members to see this number in the Troop directory."),
    )

    objects = PublishedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

    def __str__(self):
        return str(self.phone)
