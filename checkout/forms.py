from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

class CustomSignupForm(UserCreationForm):
    name = forms.CharField(max_length=100, label='Full Name')
    phone_number = forms.CharField(max_length=20, label='Phone Number')
    country = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=20, required=False)
    town_or_city = forms.CharField(max_length=100)
    street_address1 = forms.CharField(max_length=255, label='Address Line 1')
    street_address2 = forms.CharField(max_length=255, label='Address Line 2', required=False)

    # Optional delivery address
    use_different_delivery_address = forms.BooleanField(
        required=False, label='Use a different delivery address?'
    )
    delivery_country = forms.CharField(max_length=100, required=False)
    delivery_postcode = forms.CharField(max_length=20, required=False)
    delivery_town_or_city = forms.CharField(max_length=100, required=False)
    delivery_street_address1 = forms.CharField(max_length=255, required=False)
    delivery_street_address2 = forms.CharField(max_length=255, required=False)

    def save(self, request):
        user = super().save(request)

        profile = user.profile
        profile.name = self.cleaned_data['full_name']
        profile.phone_number = self.cleaned_data['phone_number']
        profile.country = self.cleaned_data['country']
        profile.postcode = self.cleaned_data['postcode']
        profile.town_or_city = self.cleaned_data['town_or_city']
        profile.street_address1 = self.cleaned_data['street_address1']
        profile.street_address2 = self.cleaned_data['street_address2']

        if self.cleaned_data.get('use_different_delivery_address'):
            profile.delivery_country = self.cleaned_data['delivery_country']
            profile.delivery_postcode = self.cleaned_data['delivery_postcode']
            profile.delivery_town_or_city = self.cleaned_data['delivery_town_or_city']
            profile.delivery_street_address1 = self.cleaned_data['delivery_street_address1']
            profile.delivery_street_address2 = self.cleaned_data['delivery_street_address2']

        profile.save()
        return user

class Meta:
    model = User
    fields = ['username', 'name', 'email', 'password1', 'password2']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
        }

        self.fields['name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False