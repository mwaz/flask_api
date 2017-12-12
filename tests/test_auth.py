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
        self.unathorized_user_details = {'email': 'uuser@unauthorized.com',
                                         'password': 'none_provided'
                                        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_register_user(self):
        """"Method to test a successful registration"""
        user_register = self.client().post('/yummy_api/v1/auth/register', data = self.user_details)
        result = json.loads(user_register.data.decode())
        self.assertEqual(result['message'], "Successfully registered")
        self.assertEqual(user_register.status_code, 201)


    def test_double_registration(self):
        """"Method to test a user who is already registered """
        user_register = self.client().post('/yummy_api/v1/auth/register', data=self.user_details)
        self.assertEqual(user_register.status_code, 201)
        double_user_registration = self.client().post('/yummy_api/v1/auth/register', data=self.user_details)
        self.assertEqual(double_user_registration.status_code, 409)


    def test_user_login(self):
        """"Method to test successful user login"""
        user_register = self.client().post('/yummy_api/v1/auth/register', data = self.user_details)
        self.assertEqual(user_register.status_code, 201)

        user_login = self.client().post('/yummy_api/v1/auth/login', data = self.user_details)
        self.assertEqual(user_login.status_code, 200)

    def test_unauthorized_login(self):
        """"Method to test unauthorized login"""
        unauthorized_login = self.client().post('/yummy_api/v1/auth/login', data=self.unathorized_user_details)
        self.assertEqual(unauthorized_login.status_code, 401)





