import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

import recurrence.fields

from trooper.members.models import Member


def get_attachment_upload(obj, filename):
    return f"calendars/{obj.uuid}/{filename}"


class Attachment(models.Model):
    uuid = models.UUIDField(
        _("UUID"), primary_key=True, editable=False, default=uuid.uuid4
    )
    title = models.CharField(_("title"), max_length=255)
    file = models.FileField(_("file"), upload_to=get_attachment_upload)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return self.title


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

    title = models.CharField(_("title"), max_length=100)
    begins_at = models.DateTimeField(_("begins"))
    ends_at = models.DateTimeField(_("ends"), blank=True, null=True)
    recurrences = recurrence.fields.RecurrenceField(blank=True)
    location = models.CharField(_("location"), max_length=255, blank=True)
    description = models.TextField(_("description"), blank=True)
    categories = models.ManyToManyField(Category, related_name="events", blank=True)
    attachments = models.ManyToManyField(Attachment, related_name="events", blank=True)
    attendees = models.ManyToManyField(
        Member, related_name="events", through="Invite", blank=True
    )
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
    rsvp_required = models.BooleanField(_("RSVP"), default=False)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    last_modified = models.DateTimeField(_("modified"), auto_now=True)
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        ordering = ["begins_at"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.ends_at and self.ends_at < self.begins_at:
            raise ValidationError(
                {"ends_at": _("An event cannot end before it begins.")}
            )

    def get_absolute_url(self):
        return reverse("calendars:detail", kwargs={"uuid": self.uuid})

    @property
    def duration(self):
        if self.ends_at:
            return self.ends_at - self.begins_at


class Invite(models.Model):
    class Role(models.TextChoices):
        CHAIR = "CHAIR", _("Chair")
        REQUIRED = "REQ-PARTICIPANT", _("Required")
        OPTIONAL = "OPT-PARTICIPANT", _("Optional")
        INFORMATIONAL = "NON-PARTICIPANT", _("Inform Only")

    class Status(models.TextChoices):
        ACCEPTED = "ACCEPTED", _("Accepted")
        DECLINED = "DECLINED", _("Declined")
        TENTATIVE = "TENTATIVE", _("Tentative")
        NO_RESPONSE = "NEEDS-ACTION", _("no response")

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(
        _("participant role"),
        max_length=15,
        choices=Role.choices,
        default=Role.REQUIRED,
    )
    status = models.CharField(
        _("response"), max_length=12, choices=Status.choices, default=Status.NO_RESPONSE
    )

    class Meta:
        verbose_name = _("Meeting Invitation")
        verbose_name_plural = _("Meeting Invitations")

    def __str__(self):
        return str(self.attendee)

    @property
    def transparency(self):
        if (
            self.role == self.Role.INFORMATIONAL
            or self.status == self.Status.DECLINED
            or self.event.status == self.event.Status.CANCELLED
        ):
            return "TRANSPARENT"
        else:
            return "OPAQUE"
