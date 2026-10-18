from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Automatically loads initial menu items into the database'

    def handle(self, *args, **kwargs):
        items = [
            {"name": "Matcha Milk Tea", "category": "Milktea", "price": 4.50},
            {"name": "Classic Iced Coffee", "category": "Coffee", "price": 3.75},
            {"name": "Croissant", "category": "Food", "price": 3.00},
        ]

        for item_data in items:
            item, created = Product.objects.get_or_create(
                name=item_data["name"],
                defaults={
                    "category": item_data["category"],
                    "price": item_data["price"],
                    "is_available": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added: {item.name}"))
            else:
                self.stdout.write(f"Item already exists: {item.name}")