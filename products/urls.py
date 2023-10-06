from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

app_name = "products"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("products/all/", views.ProductsView.as_view(), name="products"),
    path("product/<int:pk>/", views.DetailProuductView.as_view(), name="detail"),
    path(
        "products/category/<int:category_id>/",
        views.ProductsView.as_view(),
        name="category",
    ),
    path("products/page/<int:page>/", views.ProductsView.as_view(), name="paginator"),
    path("products/basket_add/<int:product_id>/", views.basket_add, name="basket_add"),
    path(
        "products/basket_remove/<int:basket_id>/",
        views.basket_remove,
        name="basket_remove",
    ),
    path(
        "products/wishlist_add/<int:product_id>/",
        views.wishlist_add,
        name="wishlist_add",
    ),
    path(
        "products/wishlist_remove/<int:wishlist_id>/",
        views.wishlist_remove,
        name="wishlist_remove",
    ),
    path(
        "products/wishlist/<int:pk>",
        login_required(views.WishListView.as_view()),
        name="wishlist",
    ),
]
