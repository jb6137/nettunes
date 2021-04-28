from catalog.models import Rental
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unittest.mock import MagicMock, Mock, patch
import catalog.views as views


class ViewTests(TestCase):
    test_user_name="Alice"
    test_user_password="password"

    def setUp(self):
        User.objects.create(username=self.test_user_name, password=self.test_user_password)

    def test_catalog_status_code(self):
        url = reverse('catalog')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_about_status_code(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_account_status_code(self):
        domain = reverse('catalog')
        url = f"/user/{self.test_user_name}"
        response = self.client.post(url, {'username': self.test_user_name, 'rentals': "", 'requests': ""})
        self.assertEquals(response.status_code, 301) # TODO: debug this test later

    def test_has_rented_max_false(self):
        user = User.objects.get(username=self.test_user_name)
        self.assertFalse(views.has_rented_max(user))
 
    def test_has_rented_max_true(self):
        mock_results = Mock()
        mock_results.__len__ = Mock(return_value=3)
        mock_rentals = Mock()
        mock_rentals.filter.return_value.exclude.return_value = mock_results
        with patch('catalog.models.Rental.objects', mock_rentals):
            user = User.objects.get(username=self.test_user_name)
            self.assertTrue(views.has_rented_max(user))

    # TODO: Add more tests for request_record, handle_record_request, queue_requests, etc. Skipping to save time.
    # At the very least - tests covering renting functionality is working correctly
    #   - tests covering queuing functionality works correctly
    #   - tests covering return of rentals, and waitlisted record requests get pulled off the queue correctly
    