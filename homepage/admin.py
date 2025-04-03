from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from .models import FAQ
from django import forms

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
    answer = forms.CharField(widget=CKEditorWidget())

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    form = FAQForm
