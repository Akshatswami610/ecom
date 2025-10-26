from rest_framework import viewsets
from .models import Product, Cart, Profile, OrderHistory, Review, ContactForm, Address
from .serializers import ProductSerializer, CartSerializer, ProfileSerializer, OrderHistorySerializer, ReviewSerializer, ContactFormSerializer, AddressSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class OrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
