from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from .models import User, EmailVerification
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from products.models import Basket
from common.views import TitleMixin


class RegisterUserView(TitleMixin, SuccessMessageMixin, CreateView):
    template_name = "users/register.html"
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users:login")
    success_message = "Вітаю, ви успішно зареєструвались"
    title = "Register"


class LoginUserView(TitleMixin, LoginView):
    template_name = "users/login.html"
    model = User
    form_class = LoginForm
    title = "Login"


class ProfileUserView(TitleMixin, UpdateView):
    template_name = "users/profile.html"
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")
    title = "Profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user.id)
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Підтвердження"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and email_verifications.first().is_expired():
            user.is_verification = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("products:index"))


@login_required()
def adminpage(request):
    pass


class OrderCreateView(TemplateView):
    template_name = 'orders/order-create.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create order'
        return context