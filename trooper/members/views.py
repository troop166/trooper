import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from trooper.members.forms import MemberChangeForm, MemberSignupForm
from trooper.members.models import Member
from trooper.members.utils import member_vcard

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
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if "filter" in self.kwargs:
            context["filter"] = self.kwargs["filter"]
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.with_published_contact_info()
        if "filter" in self.kwargs:
            filter_to = self.kwargs["filter"]
            if filter_to in self.model.objects.FILTERS_AVAILABLE:
                qs_filter = getattr(qs, filter_to)
                qs = qs_filter()
        if query := self.request.GET.get("q", default=""):
            qs = qs.search(query=query)
        return qs

    def get_template_names(self):
        if self.request.htmx:
            if self.request.GET.get("page"):
                return "members/partials/member_list_entries.html"
            return "members/partials/member_list.html"
        return self.template_name


class MemberDetailView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberChangeForm
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "members/member_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.with_published_contact_info()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members_are_related"] = self.object.is_related_to(self.request.user)
        return context


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


def member_vcard_view(request, username):
    member = get_object_or_404(Member, username=username)
    card = member_vcard(member)
    filename = f"{member.get_full_name()}.vcf"
    response = HttpResponse(card.serialize(), content_type="text/x-vcard")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
