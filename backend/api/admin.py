from django.contrib import admin
from .models import Product, Profile, OrderHistory, Review, Contact

# Register your models here.
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(OrderHistory)
admin.site.register(Review)
admin.site.register(Contact)