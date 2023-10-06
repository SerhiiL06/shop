from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from orders.views import stripe_webhook_view
from rest_framework.authtoken import views
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
    path("", include("users.urls")),
    path('accounts/', include('allauth.urls')),
    path('orders/', include("orders.urls")),
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),
    path("api/", include("api.urls")),
    path('api-token-auth/', views.obtain_auth_token)
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls"))),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
