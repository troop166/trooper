from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class MemberLoginView(LoginView):
    template_name = "members/auth/login.html"


class MemberLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        success_message = _("You have signed out successfully.")
        messages.info(request, success_message)
        return super().dispatch(request, *args, **kwargs)


class MemberPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "members/auth/password_change_form.html"
    success_message = _("Your password has been updated")
    success_url = reverse_lazy("home")


class MemberPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = "members/auth/password_reset_email.txt"
    html_email_template_name = "members/auth/password_reset_email.html"
    subject_template_name = "members/auth/password_reset_subject.txt"
    success_message = _(
        "We've emailed you instructions for resetting your password, if an "
        "account exists with the email %(email)s. If you do not receive an "
        "email, please make sure you entered the address you registered "
        "with, and check your spam folder."
    )
    success_url = reverse_lazy("home")
    template_name = "members/auth/password_reset_form.html"


class MemberPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "members/auth/password_reset_confirm.html"
    success_message = _("Your password has been updated")
    success_url = reverse_lazy("auth:login")
