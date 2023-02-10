from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.detail import SingleObjectMixin

from django_htmx.http import HttpResponseClientRedirect

from trooper.address_book.forms import AddressForm
from trooper.address_book.models import Address
from trooper.members.models import Member


class MemberMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):
        member = self.get_member()
        context = super().get_context_data(**kwargs)
        context["member"] = member
        context["members_are_related"] = member.is_related_to(self.request.user)
        return context

    def get_member(self):
        return get_object_or_404(Member, username=self.kwargs.get("username"))


class AddressListView(LoginRequiredMixin, ListView):
    model = Address

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["member"] = self.member
        context["members_are_related"] = self.member.is_related_to(self.request.user)
        return context

    def get_queryset(self):
        username = self.kwargs.get("username")
        qs = super().get_queryset()
        qs = qs.filter(member__username=username)

        if not self.member.is_related_to(self.request.user):
            qs = qs.published()
        return qs

    def get_template_names(self):
        template_names = super().get_template_names()
        if self.request.htmx:
            for i, template_name in enumerate(template_names):
                parts = template_name.split("/")
                parts.insert(len(parts) - 1, "partials")
                template_names[i] = "/".join(parts)
        return template_names

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.member = get_object_or_404(Member, username=self.kwargs.get("username"))


class AddressCreateView(
    LoginRequiredMixin, MemberMixin, SuccessMessageMixin, CreateView
):
    model = Address
    form_class = AddressForm
    template_name = "address_book/address_form.html"

    def get_success_url(self):
        if self.request.htmx:
            return reverse(
                "address_book:address_list",
                kwargs={"username": self.kwargs.get("username")},
            )
        return self.get_member().get_absolute_url()

    def get_template_names(self):
        template_names = super().get_template_names()
        if self.request.htmx:
            for i, template_name in enumerate(template_names):
                parts = template_name.split("/")
                parts.insert(len(parts) - 1, "partials")
                template_names[i] = "/".join(parts)
        return template_names

    def form_valid(self, form):
        with transaction.atomic():
            address = form.save(commit=False)
            address.content_object = self.get_member()
        return super().form_valid(form)


class AddressDetailView(LoginRequiredMixin, MemberMixin, DetailView):
    model = Address
    template_name = "address_book/address_detail.html"


class AddressUpdateView(
    LoginRequiredMixin, MemberMixin, SuccessMessageMixin, UpdateView
):
    model = Address
    form_class = AddressForm
    success_message = _("Address has been updated.")
    template_name = "address_book/address_form.html"

    def get_success_url(self):
        if self.request.htmx:
            return reverse(
                "address_book:address_list",
                kwargs={"username": self.kwargs.get("username")},
            )
        return self.get_member().get_absolute_url()

    def get_template_names(self):
        template_names = super().get_template_names()
        if self.request.htmx:
            for i, template_name in enumerate(template_names):
                parts = template_name.split("/")
                parts.insert(len(parts) - 1, "partials")
                template_names[i] = "/".join(parts)
        return template_names

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content_object = self.get_member()
        return super().form_valid(form)


class AddressDeleteView(LoginRequiredMixin, MemberMixin, DeleteView):
    model = Address
    template_name = "address_book/address_delete.html"

    def get_success_url(self):
        return self.get_member().get_absolute_url()

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_message = _("Address has been removed.")
        messages.warning(request, success_message, "danger")
        success_url = self.get_success_url()
        self.object.delete()

        if self.request.htmx:
            return HttpResponseClientRedirect(success_url)

        return HttpResponseRedirect(success_url)


# Create your views here.
def address_form_view(request, username=None, pk=None):
    member = None
    address = None

    if username and pk:
        member = get_object_or_404(Member, username=username)
        try:
            address = member.addresses.get(pk=pk)
        except Address.DoesNotExist as e:
            raise Http404 from e

    form = AddressForm(request.POST or None, instance=address)
    context = {"address": address, "form": form, "member": member}

    if address:
        context["members_are_related"] = member.is_related_to(request.user)

    template_name = "address_book/address_form.html"
    if request.htmx:
        template_name = "address_book/partials/address_form.html"

    if form.is_valid():
        with transaction.atomic():
            address = form.save(commit=False)
            if not address.content_object:
                user = request.user
                address.content_object = user
                address.save()
            if request.htmx:
                template_name = "address_book/partials/address_list_entry.html"

    return render(request, template_name, context)


def address_delete_view(request, pk=None):
    try:
        obj = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        obj = None
    if not obj:
        return HttpResponse("Not Found") if request.htmx else Http404

    if request.method == "DELETE":
        # TODO: Stay on the same page
        success_url = request.user.get_absolute_url()
        obj.delete()
        if request.htmx:
            headers = {"HX-Redirect": success_url}
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)

    context = {"obj": obj, "address": obj}
    return render(request, "address_book/address_delete.html", context)
