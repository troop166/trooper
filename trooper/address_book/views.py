from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from trooper.address_book.forms import AddressForm
from trooper.address_book.models import Address
from trooper.core.utils import check_for_htmx
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


class AddressCreateView(
    LoginRequiredMixin, MemberMixin, SuccessMessageMixin, CreateView
):
    model = Address
    form_class = AddressForm
    template_name = "address_book/address_form.html"

    def get_success_url(self):
        return self.get_member().get_absolute_url()

    def get_template_names(self):
        template_name = self.template_name
        if check_for_htmx(self.request):
            template_name = "address_book/partials/address_form.html"
        return template_name

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content_object = self.get_member()
        return super().form_valid(form)


class AddressDetailView(LoginRequiredMixin, MemberMixin, DetailView):
    model = Address
    template_name = "address_book/address_detail.html"


class AddressUpdateView(
    LoginRequiredMixin, MemberMixin, SuccessMessageMixin, UpdateView
):
    model = Address
    form_class = AddressForm
    template_name = "address_book/address_form.html"

    def get_success_url(self):
        return self.get_member().get_absolute_url()

    def get_template_names(self):
        template_name = self.template_name
        if check_for_htmx(self.request):
            template_name = "address_book/partials/address_form.html"
        return template_name

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
        success_url = self.get_success_url()
        self.object.delete()
        if check_for_htmx(self.request):
            headers = {"HX-Redirect": success_url}
            return HttpResponse("Success", headers=headers)

        return HttpResponseRedirect(success_url)


# Create your views here.
def address_form_view(request, username=None, pk=None):
    is_htmx = check_for_htmx(request)
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
    if is_htmx:
        template_name = "address_book/partials/address_form.html"

    if form.is_valid():
        with transaction.atomic():
            address = form.save(commit=False)
            if not address.content_object:
                user = request.user
                address.content_object = user
                address.save()
            if is_htmx:
                template_name = "address_book/partials/address_list_entry.html"

    return render(request, template_name, context)


def address_delete_view(request, pk=None):
    htmx = "HX-Request" in request.headers
    try:
        obj = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        obj = None
    if not obj:
        return HttpResponse("Not Found") if htmx else Http404

    if request.method == "DELETE":
        # TODO: Stay on the same page
        success_url = request.user.get_absolute_url()
        obj.delete()
        if htmx:
            headers = {"HX-Redirect": success_url}
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)

    context = {"obj": obj, "address": obj}
    return render(request, "address_book/address_delete.html", context)
