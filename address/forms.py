from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_1',
            'address_2',
            'city',
            'country',
            'state',
            'post_code',
        ]

