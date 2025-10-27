from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import (
    ProductViewSet, CartViewSet, AddressViewSet, OrderHistoryViewSet,
    ReviewViewSet, ContactViewSet, RegisterView, LoginView, ProfileView
)

router = routers.DefaultRouter()
router.register(r'Product', ProductViewSet)
router.register(r'Cart', CartViewSet)
router.register(r'Address', AddressViewSet)
router.register(r'OrderHistory', OrderHistoryViewSet)
router.register(r'Review', ReviewViewSet)
router.register(r'ContactForm', ContactViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),

    # 🔹 Authentication-related endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
