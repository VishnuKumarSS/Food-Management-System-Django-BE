from django.urls import path

from .views import (AddCartItemView, AdminOrderDetailView, AdminOrderListView,
                    CartView, OrderListCreateView)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', AddCartItemView.as_view(), name='add-cart-item'),
    
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
]
