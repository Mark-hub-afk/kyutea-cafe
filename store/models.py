from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)
    is_admin_privileged = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Coffee', 'Coffee'),
        ('Food', 'Food'),
        ('Milktea', 'Milktea'),
        ('Fruit Soda', 'Fruit Soda'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Milktea')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Add_on(models.Model):
    CLASSIFICATION_CHOICES = [
        ('Drink', 'Drink Add-on'),
        ('Pastry', 'Pastry Add-on'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default='Drink')
    image = models.ImageField(upload_to='add_ons/', blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.get_classification_display()})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=100, default='Guest')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} (₱{self.total_price})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    add_ons = models.ManyToManyField(Add_on, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for Order #{self.order.id}"

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    new_password = models.CharField(max_length=128, default='')  # Stores the pending requested password
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset request for {self.user.username}"