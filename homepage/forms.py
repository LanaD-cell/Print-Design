from django import forms
from .models import Subscriber
from django_summernote.widgets import SummernoteWidget
from .models import Newsletter

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
