import stripe

from http import HTTPStatus
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from base.settings import STRIPE_SECRET_KEY
from base import settings
from .forms import OrderForm
from django.urls import reverse_lazy, reverse
from common.views import TitleMixin
from django.views.decorators.csrf import csrf_exempt
from products.models import Basket
from orders.models import Order

stripe.api_key = STRIPE_SECRET_KEY


class SuccessOrderView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Success'


class CancelOrderView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Cancel'


class OrderListView(TitleMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    title = 'List orders'


    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    title = 'Order'
    model = Order
    template_name = 'orders/order.html'



class OrderCreateView(TitleMixin, CreateView):
    title = 'Create Order'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    model = Order
    success_url = reverse_lazy('orders:order-create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = []
        for basket in baskets:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={'order_id': self.object.id},
            mode = 'payment',
            success_url ='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success')),
            cancel_url ='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)



@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    print(payload)
    return HttpResponse(status=200)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object'],
        )


    # Fulfill the purchase...
        fulfill_order(session)
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()





