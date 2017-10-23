import unittest
from multi_credit.card.models import Card
from datetime import datetime


class CardModelsTestCase(unittest.TestCase):
    def setUp(self):

        self.card_data = {
            "number": 5165834017829286,
            "expiration_date": "2018-07-5",
            "validity_date": "2018-07-5",
            "cvv": 408,
            "limit": 2000,
            "credit": 1000
        }

    def test_pay_card(self):
        card = Card()
        value_pay = 500
        card.credit = 1000
        today = datetime.strptime("2017-05-8", "%Y-%m-%d")
        date_validate = datetime.strptime("2017-05-7", "%Y-%m-%d")
        credit = card.pay_card(
            value_pay, today, date_validate)

        self.assertEqual(credit, 1500)
