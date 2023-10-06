from .models import Product, ProductCategory, Basket, Wishlist
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = "index.html"
    title = "Index"


class ProductsView(TitleMixin, ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 3
    title = "Products"

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        context["category"] = ProductCategory.objects.filter(
            product__quantity__gt=0
        ).distinct()
        if self.request.user.is_authenticated:
            context["wishlist"] = Wishlist.objects.filter(user=self.request.user)
            return context
        else:
            context["wishlist"] = Wishlist.objects.all()
            return context

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        queryset = queryset.filter(quantity__gt=0)
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id) if category_id else queryset


class DetailProuductView(DetailView):
    template_name = "products/detail-product.html"
    model = Product


@login_required()
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def basket_remove(request, basket_id):
    product = Basket.objects.get(id=basket_id)
    product.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required()
def wishlist_add(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    wishlists = Wishlist.objects.filter(product=product, user=user)
    if not wishlists.exists():
        Wishlist.objects.create(product=product, user=user)
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


def wishlist_remove(request, wishlist_id):
    wishlist = Wishlist.objects.get(id=wishlist_id)
    wishlist.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class WishListView(TitleMixin, ListView):
    model = Wishlist
    template_name = "products/wishlist.html"
    title = "Список бажань"

    def get_queryset(self):
        queryset = super(WishListView, self).get_queryset()
        return queryset.filter(user=self.request.user)
