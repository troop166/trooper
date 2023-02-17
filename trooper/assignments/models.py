from django.db import models
from django.utils.translation import gettext as _

from trooper.assignments.managers import CommitteeQuerySet, PatrolQuerySet
from trooper.members.models import Member


class Leader(models.Model):
    class Role(models.IntegerChoices):
        MASTER = 1, _("Scoutmaster")
        ASSISTANT = 2, _("Assistant Scoutmaster")

    role = models.PositiveSmallIntegerField(_("leadership role"), choices=Role.choices)
    member = models.ForeignKey(
        Member, on_delete=models.PROTECT, limit_choices_to=Member.adult_choices
    )
    start = models.DateField(_("from"))
    end = models.DateField(_("until"), blank=True, null=True)

    class Meta:
        ordering = ["-start", "-role", "member"]
        verbose_name = _("Leader")
        verbose_name_plural = _("Leaders")

    def __str__(self):
        return _("%(role)s: %(member)s (%(start)d–%(end)s)") % {
            "role": self.get_role_display(),
            "member": self.member,
            "start": self.start.year,
            "end": self.end.year if self.end else "",
        }


class Committee(models.Model):

    name = models.CharField(_("name"), max_length=100)
    members = models.ManyToManyField(
        Member, through="CommitteeMember", related_name="committees", blank=True
    )

    objects = CommitteeQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        verbose_name = _("Committee")
        verbose_name_plural = _("Committees")

    def __str__(self):
        return self.name


class CommitteeMember(models.Model):

    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="committee_members",
        related_query_name="committee_member",
    )
    member = models.ForeignKey(
        Member,
        limit_choices_to=Member.adult_choices,
        on_delete=models.CASCADE,
        related_name="committee_members",
        related_query_name="committee_member",
    )
    start = models.DateField(_("from"))
    end = models.DateField(_("until"), blank=True, null=True)

    class Meta:
        db_table = "assignments_committee_member"
        ordering = ["-end", "member"]
        verbose_name = _("Committee Member")
        verbose_name_plural = _("Committee Members")

    def __str__(self):
        return _("%(committee)s: %(member)s (%(start)d–%(end)s)") % {
            "committee": self.committee,
            "member": self.member,
            "start": self.start.year,
            "end": self.end.year if self.end else "",
        }


class Patrol(models.Model):
    name = models.CharField(_("name"), max_length=50)
    members = models.ManyToManyField(
        Member, through="PatrolMember", related_name="patrols", blank=True
    )

    objects = PatrolQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        verbose_name = _("Patrol")
        verbose_name_plural = _("Patrols")

    def __str__(self):
        return self.name


class PatrolMember(models.Model):
    patrol = models.ForeignKey(
        Patrol,
        on_delete=models.CASCADE,
        related_name="patrol_members",
        related_query_name="patrol_member",
    )
    member = models.ForeignKey(
        Member,
        limit_choices_to=Member.youth_choices,
        on_delete=models.CASCADE,
        related_name="patrol_members",
        related_query_name="patrol_member",
    )
    start = models.DateField(_("from"))
    end = models.DateField(_("until"), blank=True, null=True)

    class Meta:
        db_table = "assignments_patrol_member"
        ordering = ["-end", "member"]
        verbose_name = _("Patrol Member")
        verbose_name_plural = _("Patrol Members")

    def __str__(self):
        return _("%(patrol)s: %(member)s (%(start)d–%(end)s)") % {
            "patrol": self.patrol,
            "member": self.member,
            "start": self.start.year,
            "end": self.end.year if self.end else "",
        }
