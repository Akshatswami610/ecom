from django.contrib import admin
from django.urls import path, include
from .views import home, aboutus, contact, profile, orders, cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', home),  # home page
    path('home', home, name='home'),  # home page
    path('aboutus', aboutus, name='aboutus'),
    path('contact', contact, name='contact'),
    path('profile', profile, name='profile'),
    path('orders', orders, name='orders'),
    path('cart', cart, name='cart'),
]
