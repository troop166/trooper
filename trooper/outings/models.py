from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext as _

from trooper.address_book.models import Address
from trooper.members.models import Member


class Outing(models.Model):
    title = models.CharField(max_length=255)
    destination = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    leaders = models.ManyToManyField(Member, through="OutingLeader")
    departs_from = models.ForeignKey(
        Address, on_delete=models.RESTRICT, related_name="+"
    )
    departs_at = models.DateTimeField()
    returns_to = models.ForeignKey(Address, on_delete=models.RESTRICT, related_name="+")
    returns_at = models.DateTimeField()

    class Meta:
        ordering = ["-departs_at"]
        verbose_name = _("Outing")
        verbose_name_plural = _("Outings")

    def __str__(self):
        return Truncator(self.title).words(15)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.returns_at < self.departs_at:
            raise ValidationError(
                {"returns_at": _("You cannot return before you depart.")}
            )


class OutingLeader(models.Model):
    class Role(models.TextChoices):
        SPONSOR = "SPONSOR", _("Sponsor")
        CO_SPONSOR = "CO_SPONSOR", _("Co-sponsor")
        SCOUTMASTER = "SCOUTMASTER", _("Scoutmaster")
        ASSISTANT = "ASSISTANT", _("Assistant Scoutmaster")
        SPL = "SPL", _("Senior Patrol Leader")
        ASPL = "ASPL", _("Assistant Senior Patrol Leader")

    outing = models.ForeignKey(Outing, on_delete=models.CASCADE)
    leader = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=Role.choices)

    class Meta:
        db_table = "outings_outing_leaders"
        constraints = [
            models.UniqueConstraint(
                fields=("outing", "leader"), name="unique_outing_leader"
            )
        ]
        verbose_name = _("Outing Leader")
        verbose_name_plural = _("Outing Leaders")

    def __str__(self):
        return _("%(role)s: %(leader)s") % {
            "role": self.get_role_display(),
            "leader": self.leader,
        }
