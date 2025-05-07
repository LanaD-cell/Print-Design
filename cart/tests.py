from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from cart.models import Cart, CartItem
from products.models import Product
from unittest.mock import patch
import json


class CartViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('19.99'),
            quantities=[{'quantity': 1, 'price': '19.99'}]
        )
        self.client.login(username='tester', password='testpass')

    def test_view_empty_cart(self):
        response = self.client.get(reverse('cart:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart is empty.")

    def test_add_to_cart_view(self):
        response = self.client.post(reverse('cart:add_to_cart'), {
            'product_id': self.product.id,
            'size': 'M',
            'quantity_option': '1',
            'services': ['Own Print Data Upload'],
        })
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)

    def test_remove_cart_item_view(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            size='M',
            quantity=1,
            price=Decimal('19.99'),
            service_price=Decimal('0.00'),
            services='[]'
        )
        response = self.client.get(reverse('cart:remove_item', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_view(self, mock_stripe_create):
        mock_stripe_create.return_value.id = 'fake_session_id'
        url = reverse('cart:create_checkout_session')
        response = self.client.post(url, json.dumps({'grand_total': '29.99'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sessionId', response.json())

    @patch('stripe.checkout.Session.retrieve')
    @patch('stripe.PaymentIntent.retrieve')
    def test_payment_success_view(self, mock_retrieve_intent, mock_retrieve_session):
        # Create a cart and add a product
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            size='M',
            quantity=1,
            price=Decimal('19.99'),
            service_price=Decimal('0.00'),
            services='[]'
        )

        # Mock the Stripe session and payment intent to simulate a successful payment
        mock_retrieve_session.return_value = {'payment_intent': 'pi_test'}
        mock_retrieve_intent.return_value.status = 'succeeded'

        # Set session with the order number
        session = self.client.session
        session['order_number'] = 'ORDER123'
        session.save()

        # Call the payment success view
        response = self.client.get(reverse('cart:payment_success') + '?session_id=fake')

        # Check if the response is successful (status 200)
        self.assertEqual(response.status_code, 200)

        # Verify the order number is shown on the page
        self.assertContains(response, 'ORDER123')
