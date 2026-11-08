from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Appeal, AppealCategory, AppealStatusHistory


class AppealTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='one@example.org', password='Password123')
        self.other = User.objects.create_user(username='two@example.org', password='Password123')
        self.category = AppealCategory.objects.create(name='Другое', slug='other')

    def test_create_and_owner_access(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('appeal-create'), {'category': self.category.pk, 'subject': 'Проблема', 'description': 'Описание'})
        appeal = Appeal.objects.get()
        self.assertContains(response, appeal.public_id)
        self.assertTrue(AppealStatusHistory.objects.filter(appeal=appeal, new_status='new').exists())
        self.assertEqual(self.client.get(reverse('appeal-detail', args=[appeal.public_id])).status_code, 200)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse('appeal-detail', args=[appeal.public_id])).status_code, 403)

    def test_unauthenticated_create_redirects(self):
        self.assertEqual(self.client.get(reverse('appeal-create')).status_code, 302)
