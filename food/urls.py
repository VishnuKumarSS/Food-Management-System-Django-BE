from django.urls import path

from .views import FoodItemDetailView, FoodItemListCreateView

urlpatterns = [
    path('food-items/', FoodItemListCreateView.as_view(), name='fooditem-list-create'),
    path('food-items/<int:pk>/', FoodItemDetailView.as_view(), name='fooditem-detail'),
]
