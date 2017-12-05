import unittest
from django.test import Client

class EventsViewTests(unittest.TestCase):
    def setUp(self):
        # Instantiate client
        self.client = Client()

    def test_details(self):

        # Issue a GET request
        get_response = self.client.get('/events/')

        # Check that the response
        self.assertEqual(get_response.status_code, 302)