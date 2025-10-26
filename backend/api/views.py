from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

from .models import (
    Product, Cart, Profile, OrderHistory,
    Review, ContactForm, Address
)
from .serializers import (
    ProductSerializer, CartSerializer, ProfileSerializer,
    OrderHistorySerializer, ReviewSerializer,
    ContactFormSerializer, AddressSerializer
)


# -----------------------------
# MODEL VIEWSETS (CRUD APIs)
# -----------------------------

class ProductViewSet(viewsets.ModelViewSet):
    """Products listing and details."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    """User cart management."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """User address management."""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """Profile model (basic CRUD, not for auth)."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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


# -----------------------------
# CUSTOM AUTHENTICATION APIS
# -----------------------------

@api_view(['POST'])
def register(request):
    """
    Register a new user using username, phone, (optional email), and password.
    Passwords are hashed before storing.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')

    # Basic validation
    if not username or not phone or not password:
        return Response({'error': 'Username, phone, and password are required'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Check duplicates
    if Profile.objects.filter(phone=phone).exists():
        return Response({'error': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)
    if email and Profile.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    # Hash password and save
    hashed_pw = make_password(password)
    serializer = ProfileSerializer(data={
        'username': username,
        'email': email,
        'phone': phone,
        'password': hashed_pw
    })

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    Login using either email or phone + password.
    """
    identifier = request.data.get('identifier')  # can be phone or email
    password = request.data.get('password')

    if not identifier or not password:
        return Response({'error': 'Both identifier and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Identify user by email or phone
        if '@' in identifier:
            user = Profile.objects.get(email=identifier)
        else:
            user = Profile.objects.get(phone=identifier)

        # Verify password
        if check_password(password, user.password):
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

    except Profile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
