from django.contrib import admin
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from .models import FAQ, Profile, Newsletter, Subscriber
from django.core.mail import send_mail
from django.utils.timezone import now


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


class NewsletterAdmin(admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'created_at', 'send_at', 'status_display')
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        """ Custom admin action to send
        selected newsletters to subscribers. """
        for newsletter in queryset:
            if newsletter.send_at and newsletter.send_at > now():
                message = (
                    f"Newsletter '{newsletter.title}' is scheduled to send "
                    f"at {newsletter.send_at}."
                )
                self.message_user(request, message)
                continue

            # If send_at is in the past or None,
            # proceed with sending the newsletter.
            recipients = [
                subscriber.email for subscriber in Subscriber.objects.all()]

            send_mail(
                subject=newsletter.title,
                message=newsletter.content,
                from_email='c.wnt.nd1053@gmail.com',
                recipient_list=recipients,
            )

            # Mark as sent and save
            newsletter.status = Newsletter.SENT
            newsletter.send_at = now()
            newsletter.save()

            message = (
                f"Newsletter '{newsletter.title}' sent to all subscribers!"
            )
            self.message_user(request, message)

    send_newsletter.short_description = (
        "Send selected newsletters to subscribers"
    )


# Register the Profile model in the admin interface
admin.site.register(Profile, ProfileAdmin)
# Register FAQ with the modified admin configuration
admin.site.register(FAQ, FAQAdmin)
# Register Subscriber
admin.site.register(Subscriber)
# Register Newsletter, NewsletterAdmin
admin.site.register(Newsletter, NewsletterAdmin)
