from django import forms
from .models import Subscriber, Newsletter, ContactRequest
from django_summernote.widgets import SummernoteWidget


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control'
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }

class ContactRequestForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ContactRequest
        fields = ['first_name', 'last_name', 'email', 'message']

