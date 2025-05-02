from django.contrib import admin
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from .models import FAQ
from .models import Profile, PrintData
from django.contrib import admin
from .models import Subscriber


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


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone_number',
        'country',
        'town_or_city',
        'street_address1',
        'postcode',
        'delivery_country',
        'delivery_town_or_city',
        'get_email'
    )

    search_fields = ('user__username', 'user__email', 'phone_number')

    list_filter = ('user', 'country')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    ordering = ('user__username',)


class PrintDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'uploaded_at', 'service_type')
    list_filter = ('service_type', 'uploaded_at')
    search_fields = ('user__username', 'product__name')


# Register the Profile model in the admin interface
admin.site.register(Profile, ProfileAdmin)
# Register FAQ with the modified admin configuration
admin.site.register(FAQ, FAQAdmin)
# Register PrintData
admin.site.register(PrintData)
admin.site.register(Subscriber)
