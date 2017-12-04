import unittest
from django.test import Client

class MapViewTests(unittest.TestCase):
    def setUp(self):
        # Instantiate client
        self.client = Client()

    def test_details(self):

        # Issue a GET request
        get_response = self.client.get('/map/')

        # Check that the response
        self.assertEqual(get_response.status_code, 302)

        #post_response = self.client.post('/profile/1/')

        #self.assertEqual(post_response.status_code, 302)