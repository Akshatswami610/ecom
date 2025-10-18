from django.contrib import admin
from .models import Product, Cart, Profile, OrderHistory, Review, Contact

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','product_variant','product_mrp')
    
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(OrderHistory)
admin.site.register(Review)
admin.site.register(Contact)