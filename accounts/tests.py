from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def test_registration_login_logout(self):
        response = self.client.post(reverse('register'), {'first_name': 'Анна', 'email': 'anna@example.org', 'password': 'StrongPass123', 'password_confirm': 'StrongPass123'})
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)
        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(reverse('profile')).status_code, 302)

    def test_forms_are_russian_and_registration_is_linked(self):
        login_page = self.client.get(reverse('login'))
        register_page = self.client.get(reverse('register'))
        self.assertContains(login_page, 'Электронная почта')
        self.assertContains(login_page, 'Пароль')
        self.assertContains(login_page, 'Зарегистрироваться')
        self.assertContains(register_page, 'Повторите пароль')
