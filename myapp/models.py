from django.core.exceptions import ValidationError
from django.db import models


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError('Must be a positive')


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_price])
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_total_price(self):
        total_price = sum(product.price for product in self.products.all())
        return total_price

    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())

