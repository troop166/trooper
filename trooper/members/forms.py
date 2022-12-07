from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.text import slugify

from trooper.members.models import Member


class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = ("first_name", "last_name", "date_of_birth")


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
            "email",
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
