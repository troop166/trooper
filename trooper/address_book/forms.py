from django import forms

from trooper.address_book.models import Address


class AddressForm(forms.ModelForm):
    error_css_class = "is-invalid"

    class Meta:
        model = Address
        fields = (
            "street",
            "street2",
            "city",
            "state",
            "zip_code",
        )
        widgets = {
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
        }


class EmailForm(forms.ModelForm):
    error_css_class = "is-invalid"

    class Meta:
        fields = ("address",)
        widgets = {
            "address": forms.EmailInput(
                attrs={"autocomplete": "email", "class": "form-control"}
            )
        }


class PhoneForm(forms.ModelForm):
    error_css_class = "is-invalid"

    class Meta:
        fields = ("number",)
        widgets = {
            "number": forms.TextInput(
                attrs={"autocomplete": "tel", "class": "form-control"}
            )
        }
