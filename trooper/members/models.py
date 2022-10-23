import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from trooper.address_book.models import Address, Email, Phone
from trooper.members.managers import MemberManager


def get_avatar_upload_to(instance, filename):
    return _("members/%(username)s/%(filename)s") % {
        "username": instance.username,
        "filename": filename,
    }


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
    email = models.EmailField(
        _("email address"),
        blank=True,
        null=True,
        error_messages={
            "unique": _("A member with that email already exists."),
        },
    )
    avatar = models.ImageField(
        _("profile picture"),
        upload_to=get_avatar_upload_to,
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
    addresses = GenericRelation(Address, related_query_name="member")
    email_addresses = GenericRelation(Email, related_query_name="member")
    phone_numbers = GenericRelation(Phone, related_query_name="member")

    objects = MemberManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "gender"]

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        if self.email:
            model_class = self.__class__
            model_class_pk = self._get_pk_val()
            field = model_class._meta.get_field("email")
            qs = model_class._default_manager.filter(email__icontains=self.email)

            if not self._state.adding and model_class_pk is not None:
                qs = qs.exclude(pk=model_class_pk)
            if qs.exists():
                raise ValidationError(
                    {
                        "email": ValidationError(
                            field.error_messages["unique"], code="unique"
                        )
                    }
                )

    def get_absolute_url(self):
        return reverse("members:detail", kwargs={"username": self.username})

    @classmethod
    def normalize_username(cls, username):
        """Ensure username is conformant and lower case."""
        return super().normalize_username(username.lower())


class Family(models.Model):
    members = models.ManyToManyField(
        Member, through="FamilyMember", related_name="families"
    )

    class Meta:
        verbose_name = _("Family")
        verbose_name_plural = _("Families")

    def __str__(self):
        return _("Unknown Family")


class FamilyMember(models.Model):
    class Role(models.TextChoices):
        PARENT = "P", _("Parent")
        CHILD = "C", _("Child")

    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(_("role"), max_length=1, choices=Role.choices)

    class Meta:
        verbose_name = _("Family Member")
        verbose_name_plural = _("Family Members")

    def __str__(self):
        return self.member.__str__()
