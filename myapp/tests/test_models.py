from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db.utils import IntegrityError

class ProductModelTest(TestCase):
    def test_valid_product_creation(self):
        temp_product = Product.objects.create(
            name='Temporary product',
            price=1.99,
            available=True
        )
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_negative_price_rejection(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Invalid product',
                price=-1.99,
                available=True
            )
            temp_product.full_clean()

    def test_missing_name_error(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name=None, price=2.99, available=True)
            temp_product.full_clean()

    def test_blank_name_error(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=2.99, available=True)
            temp_product.full_clean()

    def test_invalid_price_format_error(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Invalid price format', price=1.999, available=True)
            temp_product.full_clean()

    def test_max_name_length(self):
        edge_name = 'a' * 255
        temp_product = Product.objects.create(
            name=edge_name,
            price=5.99,
            available=True
        )
        self.assertEqual(temp_product.name, edge_name)

    def test_minimum_price_acceptance(self):
        temp_product = Product.objects.create(
            name='Min price product',
            price=0.01,
            available=True
        )
        self.assertEqual(temp_product.price, 0.01)

    def test_maximum_price_acceptance(self):
        temp_product = Product.objects.create(
            name='Max price product',
            price=999999.99,
            available=True
        )
        self.assertEqual(temp_product.price, 999999.99)


class CustomerModelTest(TestCase):
    def test_valid_customer_creation(self):
        temp_customer = Customer.objects.create(
            name="Antonio",
            address="123 Apple"
        )
        self.assertEqual(temp_customer.name, "Antonio")
        self.assertEqual(temp_customer.address, "123 Apple")

    def test_missing_name_error(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name=None, address="123 Apple")
            temp_customer.full_clean()

    def test_blank_name_error(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name="", address="123 Apple")
            temp_customer.full_clean()

    def test_missing_address_error(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name="Antonio", address=None)
            temp_customer.full_clean()

    def test_blank_address_error(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name="Antonio", address="")
            temp_customer.full_clean()

    def test_name_edge_length(self):
        edge_name = "a" * 100
        temp_customer = Customer.objects.create(
            name=edge_name,
            address="123 Apple"
        )
        self.assertEqual(temp_customer.name, edge_name)

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Antonio", address="123 Apple"
        )
        self.product1 = Product.objects.create(
            name="Orange", price=1.50, available=True
        )
        self.product2 = Product.objects.create(
            name="Mango", price=2.99, available=False
        )

    def test_valid_order_creation(self):
        order = Order.objects.create(
            customer=self.customer, status="New"
        )
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.status, "New")
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.products.count(), 2)

    def test_missing_customer_error(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(customer=None, status="New")

    def test_missing_status_error(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(customer=self.customer, status=None)

    def test_invalid_status_error(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status="Invalid Status")
            order.full_clean()

    def test_order_total_price(self):
        order = Order.objects.create(
            customer=self.customer, status="New"
        )
        order.products.add(self.product1, self.product2)
        total_price = order.calculate_total_price()
        self.assertEqual(total_price, Decimal('4.49'))  # Use Decimal

    def test_order_fulfillment_with_available_products(self):
        order = Order.objects.create(
            customer=self.customer, status="New"
        )
        order.products.add(self.product1)
        self.assertTrue(order.can_be_fulfilled())

    def test_order_fulfillment_with_unavailable_products(self):
        order = Order.objects.create(
            customer=self.customer, status="New"
        )
        order.products.add(self.product2)
        self.assertFalse(order.can_be_fulfilled())