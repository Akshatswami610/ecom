from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    product_image = models.ImageField(upload_to='Ecom/images', default='')
    product_variant = models.CharField(max_length=10, choices=PRODUCT_VARIANT)
    product_mrp = models.IntegerField(default=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_lane1 = models.CharField(max_length=100)
    address_landmark = models.CharField(max_length=50, blank=True, null=True)
    address_city = models.CharField(max_length=25)
    address_district = models.CharField(max_length=25)
    address_state = models.CharField(max_length=25)
    address_pincode = models.CharField(max_length=6)
    usercontact = models.CharField(max_length=10)

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


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name
