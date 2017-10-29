from multi_credit import app, db
import unittest
import json
from tests.helpers import TestHelper


class WalletModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
        self.client = self.app.test_client()

        self.wallet_data = {
            "max_limit": 0,
            "user_limit": 0,
            "spent_credit": 0,
            "user_id": 1
        }

        self.wallet_return = {
            "wallet": {
                "available_credit": 0,
                "id": 1,
                "max_limit": 0,
                "user_id": 1,
                "user_limit": 0
            }
        }

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_wallet(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        response_wallet = self.client.get(
            '/api/v1/wallet',
            headers=headers)
        response_message = json.loads(response_wallet.data.decode())
        self.assertEqual(response_message, self.wallet_return)
        self.assertEqual(response_wallet.status_code, 201)

    def test_user_update_limit_wallet(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        with open('tests/wallet/json/wallet_limit.json') as data_file:
            cards = json.load(data_file)
            for card in cards:
                self.client.post(
                    '/api/v1/card',
                    data=json.dumps({
                        "number": cards[card]['number'],
                        "expiration_date": "2018-07-5",
                        "validity_date": cards[card]['validity_date'],
                        "cvv": cards[card]['cvv'],
                        "limit": cards[card]['limit'],
                        "wallet_id": 1
                    }),
                    headers=headers)

        response_wallet = self.client.put(
            '/api/v1/wallet',
            data=json.dumps({
                "user_limit": 10000
            }),
            headers=headers)
        response_message = json.loads(response_wallet.data.decode())
        self.assertEqual(
            response_message['message'], "Updated limit wallet!")
        self.assertEqual(response_wallet.status_code, 201)

    def test_update_limit_above_allowed_wallet(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        with open('tests/wallet/json/wallet_limit.json') as data_file:
            cards = json.load(data_file)
            for card in cards:
                self.client.post(
                    '/api/v1/card',
                    data=json.dumps({
                        "number": cards[card]['number'],
                        "expiration_date": "2018-07-5",
                        "validity_date": cards[card]['validity_date'],
                        "cvv": cards[card]['cvv'],
                        "limit": cards[card]['limit'],
                        "wallet_id": 1
                    }),
                    headers=headers)

        response_wallet = self.client.put(
            '/api/v1/wallet',
            data=json.dumps({
                "user_limit": 13000
            }),
            headers=headers)
        response_message = json.loads(response_wallet.data.decode())
        self.assertEqual(
            response_message['message'], "Passed the limit!")
        self.assertEqual(response_wallet.status_code, 200)

    def test_purchase_value_greater_than_the_limit_reported_by_user(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        with open('tests/wallet/json/cards.json') as data_file:
            cards = json.load(data_file)
            for card in cards:
                self.client.post(
                    '/api/v1/card',
                    data=json.dumps({
                        "number": cards[card]['number'],
                        "expiration_date": "2018-07-5",
                        "validity_date": cards[card]['validity_date'],
                        "cvv": cards[card]['cvv'],
                        "limit": cards[card]['limit'],
                        "wallet_id": 1
                    }),
                    headers=headers)

        self.client.put(
            '/api/v1/wallet',
            data=json.dumps({
                "user_limit": 5000
            }),
            headers=headers)

        response_buy = self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 6000,
                'date': '2017-05-10'
            }),
            headers=headers)
        response_message = json.loads(response_buy.data.decode())

        self.assertEqual(response_message['message'], 'The user has no credit to make this purchase!')
        self.assertEqual(response_buy.status_code, 422)

    def test_purchase_value_greater_than_the_limit(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        with open('tests/wallet/json/cards.json') as data_file:
            cards = json.load(data_file)
            for card in cards:
                self.client.post(
                    '/api/v1/card',
                    data=json.dumps({
                        "number": cards[card]['number'],
                        "expiration_date": "2018-07-5",
                        "validity_date": cards[card]['validity_date'],
                        "cvv": cards[card]['cvv'],
                        "limit": cards[card]['limit'],
                        "wallet_id": 1
                    }),
                    headers=headers)

        response_buy = self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 15000,
                'date': '2017-05-10'
            }),
            headers=headers)
        response_message = json.loads(response_buy.data.decode())

        self.assertEqual(response_message['message'], 'The user has no credit to make this purchase!')
        self.assertEqual(response_buy.status_code, 422)

    def test_makes_purchase_with_a_card(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        with open('tests/wallet/json/cards.json') as data_file:
            cards = json.load(data_file)
            for card in cards:
                self.client.post(
                    '/api/v1/card',
                    data=json.dumps({
                        "number": cards[card]['number'],
                        "expiration_date": "2018-07-5",
                        "validity_date": cards[card]['validity_date'],
                        "cvv": cards[card]['cvv'],
                        "limit": cards[card]['limit'],
                        "wallet_id": 1
                    }),
                    headers=headers)

        response_buy = self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 3000,
                'date': '2017-05-10'
            }),
            headers=headers)
        response_message = json.loads(response_buy.data.decode())

        card_buy = [
            {
                'credit': 0.0,
                'number': cards['card_4']['number']
            }
        ]

        self.assertEqual(response_message['message'], card_buy)
        self.assertEqual(response_buy.status_code, 201)

    def test_makes_purchase_with_several_cards(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        with open('tests/wallet/json/cards.json') as data_file:
            cards = json.load(data_file)
            for card in cards:
                self.client.post(
                    '/api/v1/card',
                    data=json.dumps({
                        "number": cards[card]['number'],
                        "expiration_date": "2018-07-5",
                        "validity_date": cards[card]['validity_date'],
                        "cvv": cards[card]['cvv'],
                        "limit": cards[card]['limit'],
                        "wallet_id": 1
                    }),
                    headers=headers)

        response_buy = self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 4000,
                'date': '2017-05-10'
            }),
            headers=headers)
        response_message = json.loads(response_buy.data.decode())

        cards_buy = [
            {
                'credit': 0.0,
                'number': cards['card_4']['number']
            },
            {
                'credit': 1000.0,
                'number': cards['card_3']['number']
            }
        ]

        self.assertEqual(response_message['message'], cards_buy)
        self.assertEqual(response_buy.status_code, 201)

    def test_purchase_after_payment_of_a_card(self):
        TestHelper().create_user(self.client)
        response_sign_in = TestHelper().sign_in(self.client)
        auth_token = json.loads(response_sign_in.data.decode())

        headers = TestHelper().headers
        headers['x-access-token'] = auth_token['token']

        self.client.post(
            '/api/v1/card',
            data=json.dumps({
                "number": 51658340178292826,
                "expiration_date": "2018-07-5",
                "validity_date": "2017-05-5",
                "cvv": 408,
                "limit": 1000,
                "wallet_id": 1
            }),
            headers=headers)

        self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 500,
                'date': '2017-05-10'
            }),
            headers=headers)

        self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 300,
                'date': '2017-05-10'
            }),
            headers=headers)

        self.client.put(
            '/api/v1/card/pay/1',
            data=json.dumps({
                'value_pay': 300
            }),
            headers=headers)

        response_buy = self.client.put(
            '/api/v1/wallet/buy',
            data=json.dumps({
                'value': 400,
                'date': '2017-05-10'
            }),
            headers=headers)

        response_card = self.client.get(
            '/api/v1/card/1',
            headers=headers)
        response_message = json.loads(response_card.data.decode())

        self.assertEqual(response_message['card']['credit'], 100.0)
        self.assertEqual(response_buy.status_code, 201)
