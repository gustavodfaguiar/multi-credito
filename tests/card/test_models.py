from multi_credit import app, db
import unittest
import json


class CardModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
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

        self.card_data = {
            "number": 5165834017829286,
            "expiration_date": "2018-07-5",
            "validity_date": "2018-07-5",
            "cvv": 408,
            "limit": 2000
        }

        self.wallet_data = {
            "max_limit": 0,
            "user_limit": 0,
            "credit": 0,
            "user_id": 1
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_create_card(self):
        self.client.post(
            '/api/v1/user',
            data=json.dumps(self.user_data),
            headers=self.headers)

        response_login = self.client.get(
            '/api/v1/login',
            data=json.dumps(self.user_login),
            headers=self.headers)
        auth_token = json.loads(response_login.data.decode())
        self.headers['x-access-token'] = auth_token['token']

        self.client.post(
            '/api/v1/wallet',
            data=json.dumps(self.wallet_data),
            headers=self.headers)

        response = self.client.post(
            '/api/v1/card',
            data=json.dumps(self.card_data),
            headers=self.headers)
        result = json.loads(response.data.decode())

        self.assertEqual(
            result['message'], "New card created!")
        self.assertEqual(response.status_code, 201)
