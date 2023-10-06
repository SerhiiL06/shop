from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('order-create/', views.OrderCreateView.as_view(), name='order-create'),
    path('success/', views.SuccessOrderView.as_view(), name='success'),
    path('cancel/', views.CancelOrderView.as_view(), name='cancel'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail')
]
