from django.urls import reverse_lazy
from django.views.generic import CreateView

from trooper.members.forms import MemberCreationForm


class SignupView(CreateView):
    form_class = MemberCreationForm
    template_name = "members/signup.html"
    success_url = reverse_lazy("auth:login")
