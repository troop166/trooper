from django import forms

from trooper.address_book.models import Address


class AddressForm(forms.ModelForm):
    error_css_class = "is-invalid"

    class Meta:
        model = Address
        fields = (
            "label",
            "street",
            "street2",
            "city",
            "state",
            "zip_code",
            "is_published",
        )
        widgets = {
            "label": forms.Select(attrs={"class": "form-select"}),
            "street": forms.TextInput(
                attrs={"autocomplete": "address-line1", "class": "form-control"}
            ),
            "street2": forms.TextInput(
                attrs={"autocomplete": "address-line2", "class": "form-control"}
            ),
            "city": forms.TextInput(
                attrs={"autocomplete": "address-level2", "class": "form-control"}
            ),
            "state": forms.Select(
                attrs={"autocomplete": "address-level1", "class": "form-select"}
            ),
            "zip_code": forms.TextInput(
                attrs={"autocomplete": "postal-code", "class": "form-control"}
            ),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
