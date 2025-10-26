from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import (
    ProductViewSet, CartViewSet, AddressViewSet, ProfileViewSet,
    OrderHistoryViewSet, ReviewViewSet, ContactViewSet,
    login, register
)

# Routers automatically handle CRUD endpoints for ViewSets
router = routers.DefaultRouter()
router.register(r'Product', ProductViewSet)
router.register(r'Cart', CartViewSet)
router.register(r'Address', AddressViewSet)
router.register(r'Profile', ProfileViewSet)
router.register(r'OrderHistory', OrderHistoryViewSet)
router.register(r'Review', ReviewViewSet)
router.register(r'ContactForm', ContactViewSet)

# URL Patterns
urlpatterns = [
    path('admin/', admin.site.urls),

    # ViewSets (auto URLs)
    path('', include(router.urls)),

    # Custom Auth Endpoints
    path('register/', register, name='register'),
    path('login/', login, name='login'),

    # Optional: DRF's built-in API auth UI
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
