from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from homepage.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Ensure the profile is created when the user is created
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    print(f"Profile saved for {instance.username}")
