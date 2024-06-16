from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from food.models import FoodItem

from .models import Cart, CartItem, Order, OrderItem
from .serializers import (AddCartItemSerializer, CartItemSerializer,
                          CartSerializer, OrderSerializer)


class CartView(generics.RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        items_data = request.data.get('items', [])

        cart.cartitem_set.all().delete()  # Clear existing items
        for item_data in items_data:
            food_item_id = item_data.get('food_item')
            quantity = item_data.get('quantity', 0)
            
            if quantity > 0:
                food_item = get_object_or_404(FoodItem, id=food_item_id)
                CartItem.objects.create(cart=cart, food_item=food_item, quantity=quantity)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class AddCartItemView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        food_item_id = data.get('food_item')
        quantity = data.get('quantity', 1)

        if not food_item_id:
            return Response({'error': 'food_item field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        food_item = get_object_or_404(FoodItem, id=food_item_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)

        if not created:
            cart_item.quantity += int(quantity) # Increment the quantity if the item already exists
        else:
            cart_item.quantity = int(quantity)
        
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user) # It Hits OrderSerializer create() method.

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminOrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
