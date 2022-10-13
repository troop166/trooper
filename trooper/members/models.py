import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import gettext as _

from trooper.members.managers import MemberManager


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

    objects = MemberManager()

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def clean(self):
        super().clean()
        if self.email:
            model_class = self.__class__
            model_class_pk = self._get_pk_val(model_class._meta)
            field = model_class._meta.get_field("email")
            qs = model_class._default_manager.filter(email__icontains=self.email)

            params = {
                "model": self,
                "model_class": model_class,
                "model_name": capfirst(model_class._meta.verbose_name),
                "unique_chedk": (model_class, ("email",)),
                "field_label": capfirst(field.verbose_name),
            }
            if not self._state.adding and model_class_pk is not None:
                qs = qs.exclude(pk=model_class_pk)
            if qs.exists():
                raise ValidationError(
                    message=field.error_messages["unique"],
                    code="unique",
                    params=params,
                )

    @classmethod
    def normalize_username(cls, username):
        """Ensure username is conformant and lower case."""
        return super().normalize_username(username.lower())
