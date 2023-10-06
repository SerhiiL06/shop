from django.contrib import admin
from .models import ProductCategory, Product, Wishlist


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ['title', 'price']
    readonly_fields = ['title']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'quantity', 'price']
    ordering = ['title']
    search_fields = ['title']
    fields = ['title', 'price', 'quantity', 'stripe_product_price_id']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    search_fields = ['username']
    readonly_fields = ['user', 'product']





