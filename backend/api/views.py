from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .models import Product, Cart, OrderHistory, Review, ContactForm, Address
from rest_framework.decorators import action
from .serializers import (
    ProductSerializer, CartSerializer, OrderHistorySerializer,
    ReviewSerializer, ContactFormSerializer, AddressSerializer,
    RegisterSerializer, UserSerializer
)

User = get_user_model()

# -----------------------------
# MODEL VIEWSETS (CRUD APIs)
# -----------------------------

class ProductViewSet(viewsets.ModelViewSet):
    """Products listing and details."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # Products visible to everyone


class CartViewSet(viewsets.ModelViewSet):
    """Cart visible only to logged-in users."""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """Return cart items with nested product details"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'items': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """Add item to cart or update quantity if exists"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        variant = request.data.get('variant', '100g')

        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if item already exists in cart (same product + variant)
        cart_item = Cart.objects.filter(
            user=request.user,
            product=product,
            variant=variant
        ).first()

        if cart_item:
            # Update existing item quantity
            cart_item.qty += int(quantity)
            cart_item.save()
            message = 'Cart item updated'
        else:
            # Create new cart item
            cart_item = Cart.objects.create(
                user=request.user,
                product=product,
                variant=variant,
                qty=int(quantity)
            )
            message = 'Item added to cart'

        serializer = self.get_serializer(cart_item)
        return Response({
            **serializer.data,
            'message': message
        }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Update cart item quantity"""
        try:
            cart_item = self.get_queryset().get(pk=kwargs.get('pk'))
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_item.qty = int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Remove item from cart"""
        try:
            cart_item = self.get_queryset().get(pk=kwargs.get('pk'))
            cart_item.delete()
            return Response(
                {'message': 'Item removed from cart'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderHistoryViewSet(viewsets.ModelViewSet):
    """Orders and history."""
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderHistory.objects.filter(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Product reviews."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ContactViewSet(viewsets.ModelViewSet):
    """Contact form submissions."""
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# AUTH VIEWS
# -----------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = request.data.get("email") or request.data.get("phone")
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"error": "Email/Phone and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = None
        if "@" in identifier:
            user = authenticate(request, username=identifier, password=password)
        else:
            try:
                user_obj = User.objects.get(phone_number=identifier)
                if user_obj.check_password(password):
                    user = user_obj
            except User.DoesNotExist:
                pass

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
