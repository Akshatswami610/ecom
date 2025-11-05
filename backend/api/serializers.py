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


class CartProductSerializer(serializers.ModelSerializer):
    """Nested product serializer for cart items"""
    name = serializers.CharField(source='product_name')
    price = serializers.SerializerMethodField()
    image = serializers.ImageField(source='product_image')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

    def get_price(self, obj):
        # Get the variant from context if available
        variant = self.context.get('variant', '100g')
        return obj.product_price_data.get(variant, obj.product_mrp)

class CartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    quantity = serializers.IntegerField(source='qty')

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_id', 'quantity', 'variant']
        read_only_fields = ['id']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_lane1', 'address_landmark', 'address_city',
                  'address_district', 'address_state', 'address_pincode']

class OrderHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = OrderHistory
        fields = [
            'id',
            'user',
            'address',
            'product',
            'variant',
            'qty',
            'order_date',
            'delivery_date',
            'status',
            'bill_amount',
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'
