from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from .models import User, EmailVerification


class RegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'serhii', 'last_name': 'bus',
            'username': 'SerhiiBus', 'email': 'serhiibus@gmail.com',
            'password1': '12345678Qq', 'password2': '12345678Qq',
        }

    def test_register_view_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Register')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_success(self):
        user = self.data['username']
        self.assertFalse(User.objects.filter(username=user))

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=user).exists())

    def test_register_view_post_errors(self):
        user = self.data['username']
        self.assertFalse(User.objects.filter(username=user))

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=user).exists())

        email_verification = EmailVerification.objects.filter(user__username=user)
        self.assertTrue(email_verification.exists())


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:login')
        self.data = {
            'first_name': 'serhii', 'last_name': 'bus',
            'username': 'SerhiiBus', 'email': 'serhiibus@gmail.com',
            'password1': '12345678Qq', 'password2': '12345678Qq',
        }

    def test_login_view_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post(self):
        User.objects.create_user(
            username=self.data['username'],
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
            email=self.data['email'],
            password=self.data['password1']
        )
        login_data = {'username': self.data['username'], 'password': self.data['password1']}
        response = self.client.post(self.path, login_data)

        self.assertRedirects(response, reverse('products:index'))






