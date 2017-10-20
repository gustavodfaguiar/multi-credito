from multi_credit.user.models import User
from multi_credit import app, db
import unittest
import json
import jwt


class UserModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.headers = {
            'content-type': 'application/json',
            'authorization': 'Basic Z3VzdGF2b0BnbWFpbC5jb206MTIzNDU2',
            'x-access-token': ''
            }
        self.user_data = {
            "name": "Gustavo Dirceu Faria Aguiar",
            "email": "gustavo@gmail.com",
            "password": "123456"
        }

        self.user_login = {
            "username": "gustavo@gmail.com",
            "password": "123456"
        }

        with self.app.app_context():
            db.create_all()

    def test_create_user(self):
        response = self.client.post(
            '/api/v1/user',
            data=json.dumps(self.user_data),
            headers=self.headers)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], "New user created!")
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.get(
            '/api/v1/login',
            data=json.dumps(self.user_login),
            headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_get_one_user(self):
        response_login = self.client.get(
            '/api/v1/login',
            data=json.dumps(self.user_login),
            headers=self.headers)
        auth_token = json.loads(response_login.data.decode())
        self.headers['x-access-token'] = auth_token['token']

        response_user = self.client.get(
            '/api/v1/user/1',
            headers=self.headers)

        self.assertEqual(response_user.status_code, 201)
