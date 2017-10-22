from multi_credit import app, db
import unittest
import json
from tests.helpers import TestHelper


class CardModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
        self.client = self.app.test_client()

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
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        self.client.post(
            '/api/v1/wallet',
            data=json.dumps(self.wallet_data),
            headers=headers)

        response = self.client.post(
            '/api/v1/card',
            data=json.dumps(self.card_data),
            headers=headers)
        result = json.loads(response.data.decode())

        self.assertEqual(
            result['message'], "New card created!")
        self.assertEqual(response.status_code, 201)
