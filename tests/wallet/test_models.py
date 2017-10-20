from multi_credit.wallet.models import Wallet
from multi_credit import app, db
import unittest
import json
import jwt


class UserModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
        self.client = self.app.test_client()
        self.headers = {
            'content-type': 'application/json',
            'authorization': 'Basic Z3VzdGF2b0BnbWFpbC5jb206MTIzNDU2',
            'x-access-token': ''
            }
        self.wallet_data = {
            "max_limit": 0,
            "user_limit": 0,
            "credit": 0,
            "user_id": 1
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

        self.wallet_return = {
            "wallet": {
                "credit": 0,
                "id": 1,
                "max_limit": 0,
                "user_id": 1,
                "user_limit": 0
            }
        }

        with self.app.app_context():
            db.create_all()

    def test_create_wallet(self):
        response_create = self.client.post(
            '/api/v1/user',
            data=json.dumps(self.user_data),
            headers=self.headers)

        response_login = self.client.get(
            '/api/v1/login',
            data=json.dumps(self.user_login),
            headers=self.headers)
        auth_token = json.loads(response_login.data.decode())
        self.headers['x-access-token'] = auth_token['token']

        response = self.client.post(
            '/api/v1/wallet',
            data=json.dumps(self.wallet_data),
            headers=self.headers)
        result = json.loads(response.data.decode())

        self.assertEqual(
            result['message'], "New wallet created!")
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_wallet(self):

        response_login = self.client.get(
            '/api/v1/login',
            data=json.dumps(self.user_login),
            headers=self.headers)
        auth_token = json.loads(response_login.data.decode())
        self.headers['x-access-token'] = auth_token['token']

        response = self.client.post(
            '/api/v1/wallet',
            data=json.dumps(self.wallet_data),
            headers=self.headers)
        result = json.loads(response.data.decode())

        self.assertEqual(
            result['message'], "Wallet already exists!")
        self.assertEqual(response.status_code, 200)

    def test_get_wallet(self):
        response_login = self.client.get(
            '/api/v1/login',
            data=json.dumps(self.user_login),
            headers=self.headers)
        auth_token = json.loads(response_login.data.decode())
        self.headers['x-access-token'] = auth_token['token']

        response_wallet = self.client.get(
            '/api/v1/wallet',
            headers=self.headers)
        response_message = json.loads(response_wallet.data.decode())
        self.assertEqual(response_message, self.wallet_return)
        self.assertEqual(response_wallet.status_code, 201)
