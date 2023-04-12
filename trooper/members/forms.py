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

from trooper.members.models import Address, EmailAddress, Member, PhoneNumber


class MemberCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        required=False,
        help_text=_("Enter the same password as before, for verification."),
    )

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


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "label",
            "street",
            "street2",
            "city",
            "state",
            "zip_code",
            "is_published",
        )


class EmailAddressForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = ("label", "address", "is_published", "is_subscribed")


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ("label", "number", "is_published")
