from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from trooper.members.forms import MemberChangeForm, MemberSignupForm
from trooper.members.models import Member


class SignupView(CreateView):
    form_class = MemberSignupForm
    template_name = "members/signup.html"
    success_url = reverse_lazy("auth:login")


class MemberListView(ListView):
    model = Member
    template_name = "members/member_list.html"


class MemberDetailView(DetailView):
    model = Member
    slug_field = "username"
    slug_url_kwarg = "username"


class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberChangeForm
    slug_field = "username"
    slug_url_kwarg = "username"


class MemberDeleteView(DeleteView):
    model = Member
    slug_field = "username"
    slug_url_kwarg = "username"
