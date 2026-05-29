from rest_framework import serializers
from catalog.models import Product
from orders.models import Order, OrderItem
from django.contrib.auth.models import User

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    item = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', "is_paid", 'item']