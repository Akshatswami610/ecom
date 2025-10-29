from django.db import models
from django.utils import timezone
from django.conf import settings
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# -----------------------
# Custom User Manager
# -----------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """Create and save a User with email or phone number."""
        if not email and not phone_number:
            raise ValueError("User must have either an email or phone number")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)


# -----------------------
# Custom User Model
# -----------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'  # default login with phone_number
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        if self.email:
            return self.email
        return self.phone_number or "User"


# -----------------------
# Product Model
# -----------------------
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
    product_variant = MultiSelectField(choices=PRODUCT_VARIANT)
    product_mrp = models.FloatField(default=100)
    product_price_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
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


# -----------------------
# Cart Model
# -----------------------
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    variant = models.CharField(max_length=10, default='100g')  # NEW FIELD

    def __str__(self):
        return f"{self.user.email or self.user.phone_number} - {self.product.product_name} ({self.qty})"

# -----------------------
# Address Model
# -----------------------
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_lane1 = models.CharField(max_length=100)
    address_landmark = models.CharField(max_length=50, blank=True, null=True)
    address_city = models.CharField(max_length=25)
    address_district = models.CharField(max_length=25)
    address_state = models.CharField(max_length=25)
    address_pincode = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.email or self.user.phone_number}"


# -----------------------
# Order History Model
# -----------------------
class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)
    product_mrp = models.IntegerField(default=0)
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name}"


# -----------------------
# Review Model
# -----------------------
class Review(models.Model):
    STAR = [
        ("1", "★☆☆☆☆"),
        ("2", "★★☆☆☆"),
        ("3", "★★★☆☆"),
        ("4", "★★★★☆"),
        ("5", "★★★★★"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    star = models.CharField(max_length=1, choices=STAR)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.star}★"


# -----------------------
# Contact Form Model
# -----------------------
class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
