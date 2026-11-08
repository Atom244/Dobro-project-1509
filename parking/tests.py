from django.test import TestCase
from django.urls import reverse
from .models import Parking


class ParkingTests(TestCase):
    def setUp(self):
        Parking.objects.create(name='Free', address='Невский', latitude=59.9, longitude=30.3, accessible_spaces=2, paid=False)
        Parking.objects.create(name='Paid', address='Лиговский', latitude=59.9, longitude=30.4, accessible_spaces=0, paid=True)

    def test_list_and_filter(self):
        self.assertEqual(self.client.get(reverse('parking')).status_code, 200)
        response = self.client.get(reverse('parking') + '?accessible=1')
        self.assertContains(response, 'Free')
        self.assertNotContains(response, 'Paid')
