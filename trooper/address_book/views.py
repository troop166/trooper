from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from trooper.address_book.forms import AddressForm
from trooper.address_book.models import Address
from trooper.core.utils import check_for_htmx
from trooper.members.models import Member


# Create your views here.
def address_form_view(request, username=None, pk=None):
    is_htmx = check_for_htmx(request)
    address = None

    if username and pk:
        member = get_object_or_404(Member, username=username)
        try:
            address = member.addresses.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    form = AddressForm(request.POST or None, instance=address)
    context = {"form": form, "address": address}
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
