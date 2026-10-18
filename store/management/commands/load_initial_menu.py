from django.core.management.base import BaseCommand
from coffee_shop.models import MenuItem  # Change 'coffee_shop' to your actual app name if different

class Command(BaseCommand):
    help = 'Automatically loads initial menu items into the database'

    def handle(self, *args, **kwargs):
        items = [
            {"name": "Matcha Milk Tea", "category": "Drinks", "price": 4.50, "description": "Freshly brewed green tea with milk."},
            {"name": "Classic Iced Coffee", "category": "Drinks", "price": 3.75, "description": "Rich espresso with chilled milk."},
            {"name": "Croissant", "category": "Foods", "price": 3.00, "description": "Buttery, flaky French pastry."},
        ]

        for item_data in items:
            item, created = MenuItem.objects.get_or_create(
                name=item_data["name"],
                defaults={
                    "category": item_data["category"],
                    "price": item_data["price"],
                    "description": item_data["description"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added: {item.name}"))
            else:
                self.stdout.write(f"Item already exists: {item.name}")