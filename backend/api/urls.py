from django.contrib import admin
from django.urls import path, include
from api.views import ProductViewSet, ProfileViewSet, OrderHistoryViewSet, ReviewViewSet, ContactViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Product', ProductViewSet)
router.register(r'Profile', ProfileViewSet)
router.register(r'OrderHistory', OrderHistoryViewSet)
router.register(r'Review', ReviewViewSet)
router.register(r'Contact', ContactViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]