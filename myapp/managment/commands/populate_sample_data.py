from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(name='Apple', price=0.10, available=True)
        product2 = Product.objects.create(name='Orange', price=1.50, available=True)
        product3 = Product.objects.create(name='Lemon', price=2.99, available=False)

        customer1 = Customer.objects.create(name='Antonio', address='123 Apple')
        customer2 = Customer.objects.create(name='Marcus', address='456 Orange')
        customer3 = Customer.objects.create(name='Stefano', address='789 Lemon')

        order1 = Order.objects.create(customer=customer1, status='New')
        order1.products.add(product1, product2)

        order2 = Order.objects.create(customer=customer2, status='In Process')
        order2.products.add(product3)

        order3 = Order.objects.create(customer=customer3, status='Sent')
        order3.products.add(product1)

        self.stdout.write("Work!!!")
