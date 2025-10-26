from django.contrib import admin
from django.urls import path, include
from .views import home, aboutus, contact, profile, orders, cart, product, trackorder, logout, login, signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
    path('', home),  # home page
    path('home', home, name='home'),  # home page
    path('product', product, name='product'),  # home page
    path('aboutus', aboutus, name='aboutus'),
    path('contact', contact, name='contact'),
    path('profile', profile, name='profile'),
    path('orders', orders, name='orders'),
    path('cart', cart, name='cart'),
    path('trackorder', trackorder, name='trackorder'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
