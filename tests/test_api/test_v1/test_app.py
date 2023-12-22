#!/usr/bin/python3

import unittest
from api import app
import json


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_404_error_handler(self):
        response = self.app.get('/non_existent_route')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found')

    def test_default_route(self):
        response = self.app.get('/')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)

    def test_teardown_appcontext(self):
        with app.app_context():
            pass

    def test_custom_404_error(self):
        response = self.app.get('/non_existent_route_2')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found')

    def test_get_objects_route(self):
        response = self.app.get('/objects')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()
