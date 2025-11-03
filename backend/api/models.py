from django.db import models
from django.utils import timezone
from django.conf import settings
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# -----------------------
# Custom User Manager
# -----------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a user with a phone number only."""
        if not phone_number:
            raise ValueError("The phone number field must be set.")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with a phone number."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


# -----------------------
# Custom User Model
# -----------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=False, null=True, blank=True)  # only for updates, not login
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']


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
    product_desc = models.TextField(blank=True)
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

    class Meta:
        ordering = ['product_name']
        verbose_name_plural = "Products"


# -----------------------
# Cart Model
# -----------------------
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    variant = models.CharField(max_length=10, default='100g')

    @property
    def total_price(self):
        return round(self.qty * self.product.product_price_data.get(self.variant, self.product.product_mrp), 2)

    def __str__(self):
        return f"{self.user.phone_number} - {self.product.product_name} ({self.qty} x {self.variant})"

    class Meta:
        verbose_name_plural = "Carts"


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
        return f"{self.user.phone_number} - {self.address_city}"

    class Meta:
        verbose_name_plural = "Addresses"


# -----------------------
# Order History Model
# -----------------------
class OrderHistory(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    variant = models.CharField(max_length=10, default="100g")
    qty = models.PositiveIntegerField(default=1)

    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    bill_amount = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.bill_amount:
            price = self.product.product_price_data.get(self.variant, self.product.product_mrp)
            self.bill_amount = round(price * self.qty, 2)

        if self.status == "DELIVERED" and not self.delivery_date:
            self.delivery_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name} ({self.status})"

    class Meta:
        ordering = ['-order_date']
        verbose_name_plural = "Order Histories"


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

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        verbose_name_plural = "Reviews"


# -----------------------
# Contact Form Model
# -----------------------
class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contact Forms"
