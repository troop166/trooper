import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from trooper.address_book.models import Address, Email, Phone
from trooper.members.managers import FamilyQuerySet, MemberManager
from trooper.members.utils import calculate_age, get_member_photo_upload_to
from trooper.members.validators import date_of_birth_validator, date_of_death_validator


class Member(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")

    username_validator = ASCIIUsernameValidator()

    uuid = models.UUIDField(
        _("UUID"), primary_key=True, editable=False, default=uuid.uuid4
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A member with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=100)
    middle_name = models.CharField(_("middle name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100)
    suffix = models.CharField(_("suffix"), max_length=10, blank=True)
    nickname = models.CharField(
        _("nickname"),
        max_length=100,
        blank=True,
        help_text=_("The name this member prefers to be known by."),
    )
    photo = models.ImageField(
        _("profile picture"),
        upload_to=get_member_photo_upload_to,
        blank=True,
        null=True,
        help_text=_(
            "A profile photo is used in the site directory to assist members match "
            "names with faces. A good photo is one taken from the shoulders up "
            "with the face clearly visible. Photos are only available to active "
            "members and never shared outside of the Troop."
        ),
    )
    gender = models.CharField(_("gender"), max_length=1, choices=Gender.choices)
    date_of_birth = models.DateField(
        _("date of birth"), validators=[date_of_birth_validator]
    )
    date_of_death = models.DateField(
        _("date of death"), validators=[date_of_death_validator], blank=True, null=True
    )
    addresses = GenericRelation(Address, related_query_name="member")
    email_addresses = GenericRelation(Email, related_query_name="member")
    phone_numbers = GenericRelation(Phone, related_query_name="member")

    objects = MemberManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "gender", "date_of_birth"]

    class Meta:
        ordering = ["last_name", "nickname", "first_name"]
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        """
        Ensure all members get a username based on their preferred
        full name.
        """
        if not self.username:
            self.username = slugify(self.get_full_name())
        super().save(*args, **kwargs)

    def clean(self):
        """
        Override AbstractUser clean() method that tries to clean
        the no-existent email field.
        """
        pass

    def get_short_name(self):
        """
        Return either the short name for the Member.
        """
        return self.nickname or self.first_name

    def get_full_name(self):
        """
        Return the full name for the Member.
        """
        full_name = f"{self.get_short_name()} {self.last_name} {self.suffix}"
        return full_name.strip()

    def get_absolute_url(self):
        """
        Return the member detail page for the Member.
        """
        return reverse("members:detail", kwargs={"username": self.username})

    def is_related_to(self, member):
        """Returns a boolean of whether two members share a family."""
        if member == self:
            return True
        family_model = self.families.model
        return family_model.objects.filter(members=self).filter(members=member).exists()

    @property
    def email(self):
        """Returns an email address if available."""
        return self.email_addresses.first() or ""

    @classmethod
    def normalize_username(cls, username):
        """Ensure username is conformant and lower case."""
        return super().normalize_username(username.lower())

    @property
    def age(self):
        """Calculate the member's age."""
        return calculate_age(self.date_of_birth, on_date=self.date_of_death)

    @classmethod
    def adult_choices(cls):
        """
        Provides a queryset filter that can be used in other models'
        `ForeignKey` fields implementing `limit_choices_to`.

        Returns a filter including only adult members.
        """
        return {"pk__in": cls.objects.adults()}

    @classmethod
    def youth_choices(cls):
        """
        Provides a queryset filter that can be used in other models'
        `ForeignKey` fields implementing `limit_choices_to`.

        Returns a filter including only youth members.
        """
        return {"pk__in": cls.objects.youths()}


class Family(models.Model):
    members = models.ManyToManyField(
        Member, through="FamilyMember", related_name="families"
    )

    objects = FamilyQuerySet.as_manager()

    class Meta:
        verbose_name = _("Family")
        verbose_name_plural = _("Families")

    def __str__(self):
        if not self.members.count():
            return _("new family")
        names = (
            self.members.exclude(last_name="")
            .order_by("last_name")
            .values_list("last_name", flat=True)
        )
        return _("%s Family") % "/".join(set(names)) if names else _("Unknown Family")


class FamilyMember(models.Model):
    class Role(models.TextChoices):
        PARENT = "P", _("Parent")
        CHILD = "C", _("Child")

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name="family_members",
        related_query_name="family_member",
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(_("role"), max_length=1, choices=Role.choices)

    class Meta:
        db_table = "members_family_member"
        verbose_name = _("Family Member")
        verbose_name_plural = _("Family Members")

    def __str__(self):
        return self.member.__str__()
