from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payment intent"""
        payment_intent = event['data']['object']
        order_number = payment_intent.get('metadata', {}).get('order_number')

        logger.info(f'PaymentIntent for order {order_number} succeeded.')

        return HttpResponse(status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payment intent"""
        payment_intent = event['data']['object']
        order_number = payment_intent.get('metadata', {}).get('order_number')

        logger.warning(f'PaymentIntent for order {order_number} failed.')

        return HttpResponse(status=200)