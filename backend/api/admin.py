from django.contrib import admin
from .models import Product, Cart, OrderHistory, Review, ContactForm, Address, CustomUser

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','product_variant','product_mrp')


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(OrderHistory)
admin.site.register(Review)
admin.site.register(ContactForm,ContactFormAdmin)
admin.site.register(CustomUser)