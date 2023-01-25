from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from trooper.address_book.forms import AddressForm
from trooper.address_book.models import Address


# Create your views here.
def address_form_view(request, pk=None):
    form = AddressForm(request.POST or None)
    context = {"form": form}
    template_name = "address_book/address_form.html"
    if "HX-Request" in request.headers:
        template_name = "address_book/partials/address_form.html"

    if form.is_valid():
        with transaction.atomic():
            user = request.user
            address = form.save(commit=False)
            address.content_object = user
            address.save()

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
