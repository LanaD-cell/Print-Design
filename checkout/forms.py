from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from homepage.models import Profile
from .models import Order


class CustomSignupForm(UserCreationForm):
    # User fields
    name = forms.CharField(max_length=100, label='Full Name', required=True)
    email = forms.EmailField(max_length=100, label='Email Address', required=True)
    phone_number = forms.CharField(max_length=20, label='Phone Number', required=True)
    street_address1 = forms.CharField(max_length=255, label='Address Line 1', required=True)
    street_address2 = forms.CharField(
        max_length=255, label='Address Line 2', required=False)
    postcode = forms.CharField(max_length=20, required=True)
    town_or_city = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "The two password fields must match.")
            else:
                self.confirm_password_success = "✔ Passwords match."

        return cleaned_data

    # Optional delivery address
    use_different_delivery_address = forms.BooleanField(
        required=False, label='Use a different delivery address?'
    )
    delivery_country = forms.CharField(max_length=100, required=False)
    delivery_postcode = forms.CharField(max_length=20, required=False)
    delivery_town_or_city = forms.CharField(max_length=100, required=False)
    delivery_street_address1 = forms.CharField(max_length=255, required=False)
    delivery_street_address2 = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']

        if commit:
            user.save()

        # Create and save the profile data
        profile = Profile.objects.create(user=user)
        profile.phone_number = self.cleaned_data['phone_number']
        profile.country = self.cleaned_data['country']
        profile.postcode = self.cleaned_data['postcode']
        profile.town_or_city = self.cleaned_data['town_or_city']
        profile.street_address1 = self.cleaned_data['street_address1']
        profile.street_address2 = self.cleaned_data['street_address2']

        # If a different delivery address is provided, save it
        if self.cleaned_data.get('use_different_delivery_address'):
            profile.delivery_country = self.cleaned_data['delivery_country']
            profile.delivery_postcode = self.cleaned_data['delivery_postcode']
            profile.delivery_town_or_city = self.cleaned_data[
                'delivery_town_or_city']
            profile.delivery_street_address1 = self.cleaned_data[
                'delivery_street_address1']
            profile.delivery_street_address2 = self.cleaned_data[
                'delivery_street_address2']

        if commit:
            profile.save()

        return user


class Meta:
    model = User
    fields = ['username', 'name', 'email', 'password1', 'password2']


class OrderForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    street_address1 = forms.CharField(required=True)
    street_address2 = forms.CharField(required=False)
    town_or_city = forms.CharField(required=True)
    postcode = forms.CharField(required=True)
    country = forms.CharField(required=True)

    class Meta:
        model = Order
        fields = ('name', 'email', 'phone_number', 'print_data_file',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country')

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
            if field != 'print_data_file':
                placeholder = placeholders.get(field, '')
                if self.fields[field].required:
                    placeholder = f'{placeholder} *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False

        if self.instance.print_data_file:
            # Display the uploaded file name in the placeholder
            self.fields['print_data_file'].widget.attrs[
                'placeholder'] = f"File uploaded: {
                    self.instance.print_data_file.name}"
            self.fields['print_data_file'].widget.attrs['readonly'] = True


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    address_line_1 = forms.CharField(max_length=255, required=True)
    address_line_2 = forms.CharField(max_length=255, required=False)
    town_or_city = forms.CharField(max_length=100, required=True)
    postcode = forms.CharField(max_length=10, required=True)
    country = forms.CharField(max_length=100, required=True)
    use_different_delivery_address = forms.BooleanField(required=False)
    delivery_street_address_1 = forms.CharField(max_length=255, required=False)
    delivery_street_address_2 = forms.CharField(max_length=255, required=False)
    delivery_town_or_city = forms.CharField(max_length=100, required=False)
    delivery_postcode = forms.CharField(max_length=10, required=False)
    delivery_country = forms.CharField(max_length=100, required=False)