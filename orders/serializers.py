from rest_framework import serializers

from food.models import FoodItem
from food.serializers import FoodItemSerializer

from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'food_item', 'quantity']


class CartItemUpdateSerializer(serializers.ModelSerializer):
    food_item = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'food_item', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer(many=True, source='cartitem_set')
    items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['food_item', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    food_item = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    items_list = OrderItemSerializer(many=True, source='orderitem_set', read_only=True)

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items_list', 'items']
        read_only_fields = ['id', 'created_at', 'user', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        order = Order.objects.create(user=user)
        
        for item_data in items_data:
            food_item = item_data.get('food_item')
            
            if food_item:
                quantity = item_data.get('quantity')
                food_item.quantity_available -= quantity
                food_item.quantity_sold += quantity
                food_item.save()
            
            OrderItem.objects.create(order=order, **item_data)
        
        return order