from django.contrib import admin
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from .models import FAQ

# Custom form for FAQ to use in the admin interface
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'

    # Make sure 'answer' is a CharField and will use Summernote
    answer = forms.CharField(widget=forms.Textarea)

# Use Summernote for the FAQ admin
class FAQAdmin(SummernoteModelAdmin):
    summernote_fields = ('answer',)
    list_display = ('question',)

# Register FAQ with the modified admin configuration
admin.site.register(FAQ, FAQAdmin)