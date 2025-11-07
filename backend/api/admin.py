from django.contrib import admin
from .models import Product, Cart, OrderHistory, Review, ContactForm, Address, CustomUser


# ------------------- Product Admin -------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_variant', 'product_mrp', 'timestamp')
    search_fields = ('product_name', 'product_variant')


# ------------------- Cart Admin -------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'qty', 'variant')
    search_fields = ('user__phone_number', 'product__product_name')


# ------------------- Address Admin -------------------
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_city', 'address_district', 'address_state', 'address_pincode')
    search_fields = ('user__phone_number', 'address_city', 'address_district', 'address_state')


# ------------------- Order History Admin -------------------
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'qty', 'status', 'bill_amount', 'order_date')
    search_fields = ('user__phone_number', 'product__product_name', 'status')


# ------------------- Review Admin -------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'star', 'created_at')
    search_fields = ('product__product_name', 'user__phone_number')


# ------------------- Contact Form Admin -------------------
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')


# ------------------- Custom User Admin -------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'date_joined', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name')
