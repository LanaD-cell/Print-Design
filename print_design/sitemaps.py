from django.contrib.sitemaps import Sitemap
from products.models import Product, Category, ProductSize, QuantityOption
from cart.models import Cart, CartItem
from checkout.models import Order, OrderLineItem
from homepage.models import FAQ, PrintData, Profile, Subscriber, Newsletter


class GenericModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        """
        Returns the queryset of the model.
        Update this method for models with specific query needs.
        """
        return self.model.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def __init__(self, model):
        self.model = model


# Define the sitemaps for each model
sitemaps = {
    'products': GenericModelSitemap(Product),
    'faqs': GenericModelSitemap(FAQ),
    'profiles': GenericModelSitemap(Profile),
    'subscribers': GenericModelSitemap(Subscriber),
    'newsletters': GenericModelSitemap(Newsletter),
    'categories': GenericModelSitemap(Category),
    'product_sizes': GenericModelSitemap(ProductSize),
    'quantity_options': GenericModelSitemap(QuantityOption),
    'carts': GenericModelSitemap(Cart),
    'cart_items': GenericModelSitemap(CartItem),
    'orders': GenericModelSitemap(Order),
    'order_line_items': GenericModelSitemap(OrderLineItem),
}
