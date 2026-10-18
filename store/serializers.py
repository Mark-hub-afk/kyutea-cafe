from rest_framework import serializers
from .models import CustomUser, Product, Add_on, Order, OrderItem, PasswordResetRequest

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_approved', 'is_admin_privileged', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'is_available', 'image']

class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_on
        fields = ['id', 'name', 'price', 'classification', 'image']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    add_ons_detail = AddOnSerializer(source='add_ons', many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'add_ons', 'add_ons_detail']

class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'add_ons']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    items_data = OrderItemWriteSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'total_price', 'status', 'created_at', 'items', 'items_data']

    def create(self, validated_data):
        items_data = validated_data.pop('items_data', [])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            add_ons = item_data.pop('add_ons', [])
            order_item = OrderItem.objects.create(order=order, **item_data)
            if add_ons:
                order_item.add_ons.set(add_ons)

        return order

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PasswordResetRequest
        fields = ['id', 'user', 'username', 'requested_at', 'is_approved']