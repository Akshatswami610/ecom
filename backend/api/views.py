from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Product, Cart, OrderHistory, Review, ContactForm, Address
from .serializers import ProductSerializer, CartSerializer, OrderHistorySerializer, ReviewSerializer, ContactFormSerializer, AddressSerializer

# -----------------------------
# MODEL VIEWSETS (CRUD APIs)
# -----------------------------

class ProductViewSet(viewsets.ModelViewSet):
    """Products listing and details."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """User address management."""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OrderHistoryViewSet(viewsets.ModelViewSet):
    """Orders and history."""
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Product reviews."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """Contact form submissions."""
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
