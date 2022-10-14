from django import forms

from trooper.address_book.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "label",
            "street",
            "street2",
            "city",
            "state",
            "zipcode",
            "is_published",
        )
        widgets = {
            "street": forms.TextInput(attrs={"autocomplete": "address-line1"}),
            "street2": forms.TextInput(attrs={"autocomplete": "address-line2"}),
            "city": forms.TextInput(attrs={"autocomplete": "address-level2"}),
            "state": forms.Select(attrs={"autocomplete": "address-level1"}),
            "zipcode": forms.TextInput(attrs={"autocomplete": "postal-code"}),
        }
