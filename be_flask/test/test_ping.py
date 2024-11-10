# python -m unittest test.test_ping

import unittest
from unittest.mock import patch

from main import app 


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
    
    def test_ping(self):
        response = self.client.get("/api/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('ping'), 'pong')


