import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from trooper.members.forms import MemberChangeForm, MemberSignupForm
from trooper.members.models import Member

logger = logging.getLogger(__name__)


class SignupView(SuccessMessageMixin, CreateView):
    form_class = MemberSignupForm
    template_name = "members/signup.html"
    success_message = _(
        "An account has been created for <strong>%(first_name)s</strong>."
    )
    success_url = reverse_lazy("auth:login")


class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = "members/member_list.html"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q", default="")
        if query:
            return qs.search(query=query)
        return qs

    def get_template_names(self):
        if "HX-Request" in self.request.headers:
            return "members/partials/member_list_entries.html"
        return self.template_name


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.with_published_contact_info()


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberChangeForm
    slug_field = "username"
    slug_url_kwarg = "username"
    success_message = _(
        "Member <strong>%(member)s</strong> has been successfully updated."
    )


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = reverse_lazy("members:list")

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        success_message = (
            _(
                "Member <strong>%s</strong> has been permanently removed "
                "from the database."
            )
            % self.object
        )
        self.object.delete()
        messages.warning(request, success_message)
        logger.info(_("%s was deleted by %s") % (self.object, request.user))
        return HttpResponseRedirect(success_url)
