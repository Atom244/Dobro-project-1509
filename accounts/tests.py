from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def test_registration_login_logout(self):
        response = self.client.post(reverse('register'), {'first_name': 'Анна', 'email': 'anna@example.org', 'password': 'StrongPass123', 'password_confirm': 'StrongPass123'})
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)
        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(reverse('profile')).status_code, 302)
