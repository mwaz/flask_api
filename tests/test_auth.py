"""Tests for User Authentication"""
import unittest
import json
from app import db, make_app

class TestAuth(unittest.TestCase):
    """"Testcase for blueprint for authentication"""

    def setUp(self):
        self.app = make_app(config_name="testing")
        self.client = self.app.test_client
        self.user_details = {'email':'someone@gmail.com',
                             'password':'testing_p@ssword'
                             }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def testResisterUser(self):
        user_register = self.client.post('/flask_api/v1/auth/register', data = self.user_details)
        result = json.loads(user_register.data.decode())
        self.assertEqual(result['message'], "Successfully registered")
        self.assertEqual(user_register.status_code, 201)
