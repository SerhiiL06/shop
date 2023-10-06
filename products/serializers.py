from rest_framework import serializers, fields
from .models import Product, ProductCategory, Basket


class ProductSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'quantity', 'created_at', 'category']


class BasketSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    sum = fields.FloatField()

    class Meta:
        model = Basket
        fields = ['id', 'product', 'quantity', 'created_timestamp', 'sum']
        read_only_fields = ['created_timestamp']