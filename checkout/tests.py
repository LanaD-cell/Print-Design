from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from products.models import Product
from checkout.models import Order
from decimal import Decimal
from unittest.mock import patch

class CheckoutViewTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create product
        self.product = Product.objects.create(name='Test Product', price=Decimal('20.00'))
        # Create cart and add items
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_checkout_view_with_items(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('checkout:order_checkout'))
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_without_items(self):
        self.cart.items.all().delete()
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('checkout:order_checkout'))
        self.assertRedirects(response, reverse('homepage'))

class CreateOrderViewTestCase(TestCase):
    def setUp(self):
        # Create user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a product and add to the cart
        self.product = Product.objects.create(name='Test Product', price=Decimal('20.00'))
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_create_order(self):
        response = self.client.post(reverse('checkout:create_order'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '123456789',
            'country': 'Country',
            'postcode': '12345',
            'town_or_city': 'City',
            'street_address1': 'Address Line 1',

        })

        self.assertEqual(response.status_code, 302)  #
        self.assertTrue(Order.objects.filter(user=self.user).exists())

class CreateCheckoutSessionTestCase(TestCase):
    def setUp(self):
        # Create user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a product and add to the cart
        self.product = Product.objects.create(name='Test Product', price=Decimal('20.00'))
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_create_checkout_session(self):
        response = self.client.post(reverse('checkout:create_checkout_session'), {
            'grand_total': 20.00,
            'order_number': '12345',
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('sessionId', response_data)

class PaymentSuccessViewTestCase(TestCase):
    def setUp(self):
        # Create user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a product and add to the cart
        self.product = Product.objects.create(name='Test Product', price=Decimal('20.00'))
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        # Create an order
        self.order = Order.objects.create(
            user=self.user,
            order_number='12345',
            order_total=Decimal('20.00'),
            cart_total=Decimal('20.00'),
            service_cost=Decimal('0.00'),
            delivery_cost=Decimal('0.00'),
            grand_total=Decimal('20.00')
        )

    @patch('stripe.checkout.Session.retrieve')
    def test_payment_success(self, mock_retrieve):
        # Mock the stripe session retrieve to simulate a successful payment
        mock_retrieve.return_value = {
            'client_reference_id': '12345',
            'payment_status': 'paid'
        }

        response = self.client.get(reverse('checkout:payment_success', kwargs={'order_number': '12345'}), {
            'session_id': 'test_session_id'
        })

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Paid')
        self.assertContains(response, 'Payment successful! Your order number is 12345')

