from django.urls import path, include
from . import views
from rest_framework import  routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', views.ProductListAPIView)
router.register(r'baskets', views.BasketAPIViewSet)

urlpatterns = [
    path('', include(router.urls))
]