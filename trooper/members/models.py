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
    addresses = GenericRelation(Address, related_query_name="member")
    email_addresses = GenericRelation(Email, related_query_name="member")
    phone_numbers = GenericRelation(Phone, related_query_name="member")

    objects = MemberManager()

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

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
