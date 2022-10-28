import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from trooper.members.models import Member


def get_attachment_upload(obj, filename):
    return f"{obj.uuid}/{filename}"


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Event(models.Model):
    class Status(models.TextChoices):
        TENTATIVE = "TENTATIVE", _("Tentative")
        CONFIRMED = "CONFIRMED", _("Confirmed")
        CANCELLED = "CANCELLED", _("Canceled")

    summary = models.CharField(_("summary"), max_length=100)
    begins_at = models.DateTimeField(_("begins"))
    ends_at = models.DateTimeField(_("ends"), blank=True, null=True)
    description = models.TextField(_("description"), blank=True)
    categories = models.ManyToManyField(Category, related_name="events")
    url = models.URLField(_("URL"), blank=True)

    # Metadata fields
    organizer = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="events_organized",
        related_query_name="organized_event",
    )
    status = models.CharField(
        _("status"), max_length=9, choices=Status.choices, default=Status.CONFIRMED
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    last_modified = models.DateTimeField(_("modified"), auto_now=True)
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        ordering = ["begins_at"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.summary

    def clean(self):
        super().clean()
        if self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError(
                {"ends_at": _("An event cannot end before it begins.")}
            )


class Attachment(models.Model):
    uuid = models.UUIDField(
        _("UUID"), primary_key=True, editable=False, default=uuid.uuid4
    )
    title = models.CharField(_("title"), max_length=255)
    file = models.FileField(_("file"), upload_to=get_attachment_upload)
    event = models.ManyToManyField(Event, related_name="attachments")

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return self.title


class Invite(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Member, on_delete=models.CASCADE)
