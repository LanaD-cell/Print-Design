from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from homepage.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create Userprofile
        Profile.objects.create(user=instance)
    else:
        # Update Userprofile
        instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the user profile whenever the user is saved.
    """
    instance.profile.save()