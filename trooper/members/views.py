from django.urls import reverse_lazy
from django.views.generic import CreateView

from trooper.members.forms import MemberSignupForm


class SignupView(CreateView):
    form_class = MemberSignupForm
    template_name = "members/signup.html"
    success_url = reverse_lazy("auth:login")
