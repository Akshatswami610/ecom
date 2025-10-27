from django.urls import path, include
from rest_framework import routers
from api.views import ProductViewSet, CartViewSet, AddressViewSet, OrderHistoryViewSet, ReviewViewSet, ContactViewSet

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
    path('', include(router.urls))
]
