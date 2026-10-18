import os
from django.core.management.base import BaseCommand
from store.models import CustomUser

class Command(BaseCommand):
    help = 'Automatically creates an admin user with full privileges'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword123')

        user, created = CustomUser.objects.get_or_create(username=username, defaults={'email': email})

        # Force set admin privileges and approval status
        user.set_password(password)
        user.is_approved = True
        user.is_admin_privileged = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created admin user: {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Successfully updated admin user: {username} with full privileges"))