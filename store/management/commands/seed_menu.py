from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with authentic KyuTea menu items'

    def handle(self, *args, **kwargs):
        products = [
            {"name": "Okinawa Deluxe", "price": 134.00},
            {"name": "Roasted Wintermelon", "price": 134.00},
            {"name": "Cookie Rebel Cremé", "price": 134.00},
            {"name": "Caramel Macchiato", "price": 184.00},
            {"name": "Muscovado Seasalt Latte", "price": 170.00},
            {"name": "Coated Fries", "price": 169.00},
            {"name": "Kuchi Beef Quesadilla", "price": 199.00},
        ]

        for p in products:
            Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "price": p["price"]
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded KyuTea menu items!'))