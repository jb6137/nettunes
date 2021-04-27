from django.test import TestCase
from django.urls import reverse


class ViewTests(TestCase):
    def test_catalog_status_code(self):
        url = reverse('catalog')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_about_status_code(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

