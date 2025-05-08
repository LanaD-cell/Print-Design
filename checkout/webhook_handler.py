from django.http import HttpResponse
from checkout.models import Order


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

        return HttpResponse(status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payment intent"""
        payment_intent = event['data']['object']
        order_number = payment_intent.get('metadata', {}).get('order_number')

        return HttpResponse(status=200)

    def handle_checkout_session_completed(self, event):
        """Handle the checkout.session.completed webhook from Stripe"""
        session = event['data']['object']
        session_id = session.get('id')
        order_id = session.get('client_reference_id')
        payment_status = session.get('payment_status')

        if not order_id:
            return HttpResponse(status=400)

        try:
            order = Order.objects.get(id=order_id)
            if payment_status == 'paid':
                order.status = 'Paid'
                order.save()

            else:
                pass

        except Order.DoesNotExist:
            return HttpResponse(status=404)

        return HttpResponse(status=200)
