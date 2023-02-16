from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.text import slugify
from django.utils.translation import gettext as _

from trooper.members.models import Member


class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = ("first_name", "last_name", "date_of_birth", "gender")


class MemberChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Member


class MemberAuthenticationForm(AuthenticationForm):
    pass


class MemberSignupForm(MemberCreationForm):
    class Meta:
        model = Member
        fields = (
            "first_name",
            "last_name",
            "gender",
        )
        widgets = {"gender": forms.RadioSelect(attrs={"class": "form-check-input"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].choices = Member.Gender.choices

    def save(self, commit=True):
        member = super().save(commit=False)
        member.username = slugify(f"{member.first_name} {member.last_name}")
        if commit:
            member.save()
        return member


class MemberInvitationForm(PasswordResetForm):
    """
    Leverage Django's built-in PasswordResetForm to allow Members to invite
    additional family members into the Troop.
    """

    pass
