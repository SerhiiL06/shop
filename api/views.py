from rest_framework.viewsets import ModelViewSet
from products.models import Product, Basket
from products.serializers import ProductSerializers, BasketSerializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class ProductListAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super(ProductListAPIView, self).get_permissions()


class BasketAPIViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializers
    permission_classes = [IsAuthenticated]
