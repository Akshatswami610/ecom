from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


class Product(models.Model):
    PRODUCT_VARIANT = [
        ("100g", "100g"),
        ("200g", "200g"),
        ("500g", "500g"),
        ("1kg", "1kg"),
        ("2kg", "2kg"),
        ("5kg", "5kg"),
    ]

    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='ecom/images/', default='')

    # 🔹 Keep the same name but make it multiselect
    product_variant = MultiSelectField(choices=PRODUCT_VARIANT)

    # 🔹 Keep the same name for MRP (base price = 100g)
    product_mrp = models.FloatField(default=100)

    # 🔹 New field to store calculated prices
    product_price_data = models.JSONField(default=dict, blank=True)

    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Define conversion ratios based on 100g
        conversion = {
            "100g": 1,
            "200g": 2,
            "500g": 5,
            "1kg": 10,
            "2kg": 20,
            "5kg": 50,
        }

        prices = {}
        for variant in self.product_variant:
            if variant in conversion:
                prices[variant] = round(self.product_mrp * conversion[variant], 2)

        self.product_price_data = prices
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.qty})"


class Profile(models.Model):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=10, unique=True, default='0000000000')
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_lane1 = models.CharField(max_length=100)
    address_landmark = models.CharField(max_length=50, blank=True, null=True)
    address_city = models.CharField(max_length=25)
    address_district = models.CharField(max_length=25)
    address_state = models.CharField(max_length=25)
    address_pincode = models.CharField(max_length=6)
    def __str__(self):
        return self.user.username

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)
    product_mrp = models.IntegerField(default=0)
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name}"


class Review(models.Model):
    STAR = [
        ("1", "★☆☆☆☆"),
        ("2", "★★☆☆☆"),
        ("3", "★★★☆☆"),
        ("4", "★★★★☆"),
        ("5", "★★★★★"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.CharField(max_length=1, choices=STAR)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.star}★"


class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name