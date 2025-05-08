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
        print(f"Webhook received: {event['type']}")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payment intent"""
        payment_intent = event['data']['object']
        order_number = payment_intent.get('metadata', {}).get('order_number')

        if order_number:
            try:
                order = Order.objects.get(order_number=order_number)
                order.status = 'Paid'
                order.save()
                print(f"Order {order_number} marked as Paid")
            except Order.DoesNotExist:
                print(f"Order with number {order_number} does not exist.")
        else:
            print("No order_number found in payment intent metadata.")

        return HttpResponse(status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payment intent"""
        payment_intent = event['data']['object']
        order_number = payment_intent.get('metadata', {}).get('order_number')

        if order_number:
            try:
                order = Order.objects.get(order_number=order_number)
                order.status = 'Payment Failed'
                order.save()
                print(f"Order {order_number} marked as Payment Failed")
            except Order.DoesNotExist:
                print(f"Order with number {order_number} does not exist.")
        else:
            print("No order_number found in payment intent metadata.")

        return HttpResponse(status=200)

    def handle_checkout_session_completed(self, event):
        """Handle the checkout.session.completed webhook from Stripe"""
        session = event['data']['object']
        session_id = session.get('id')
        order_id = session.get('client_reference_id')
        payment_status = session.get('payment_status')

        if not order_id:
            print("No order_id found in session object.")
            return HttpResponse(status=400)

        try:
            order = Order.objects.get(id=order_id)
            if payment_status == 'paid':
                order.status = 'Paid'
                order.save()
                print(f"Order {order_id} marked as Paid.")
            else:
                order.status = 'Payment Failed'
                order.save()
                print(f"Order {order_id} payment failed.")

        except Order.DoesNotExist:
            print(f"Order with ID {order_id} does not exist.")
            return HttpResponse(status=404)

        return HttpResponse(status=200)
