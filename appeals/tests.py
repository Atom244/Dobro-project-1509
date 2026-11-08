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

    def test_staff_dashboard_is_restricted_and_updates_status(self):
        self.assertEqual(self.client.get(reverse('staff-dashboard')).status_code, 302)
        appeal = Appeal.objects.create(user=self.user, category=self.category, subject='Проверка', description='Текст')
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('staff-dashboard')).status_code, 302)
        admin = User.objects.create_superuser(username='admin@example.org', password='Password123', email='admin@example.org')
        self.client.force_login(admin)
        self.assertEqual(self.client.get(reverse('staff-dashboard')).status_code, 200)
        response = self.client.post(reverse('staff-update', args=[appeal.public_id]), {'status': 'in_progress', 'comment': 'Передано в работу'})
        self.assertRedirects(response, reverse('staff-dashboard'))
        appeal.refresh_from_db()
        self.assertEqual(appeal.status, 'in_progress')
        self.assertTrue(AppealStatusHistory.objects.filter(appeal=appeal, new_status='in_progress', comment='Передано в работу').exists())
