from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem

print("checkout.signals has been loaded")


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    # Debugging
    print(f"post_save signal triggered for {instance}")
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    # Debugging
    print(f"post_delete signal triggered for {instance}")
    """
    Update order total on lineitem delete
    """
    print('delete signal received!')
    instance.order.update_total()