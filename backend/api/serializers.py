from rest_framework import serializers
from api.models import Product, Cart, OrderHistory, Review, ContactForm, Address
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    agree_terms = serializers.BooleanField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'agree_terms',
        ]

    def validate(self, attrs):
        # ✅ Check password match
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Passwords do not match"})

        # ✅ Check agree_terms
        if not attrs.get('agree_terms'):
            raise serializers.ValidationError({"agree_terms": "You must agree to the Terms and Privacy Policy."})

        return attrs

    def create(self, validated_data):
        # Remove fields not in User model
        validated_data.pop('confirm_password', None)
        validated_data.pop('agree_terms', None)

        # Create user
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"