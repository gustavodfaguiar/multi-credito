import unittest
from multi_credit.card.models import Card


class CardUnitModelsTestCase(unittest.TestCase):
    def setUp(self):

        self.card_data = {
            "number": 5165834017829286,
            "expiration_date": "2018-07-5",
            "validity_date": 5,
            "cvv": 408,
            "limit": 2000,
            "credit": 1000
        }

    def test_pay_card(self):
        card = Card()
        value_pay = 500
        card.credit = 1000
        credit = card.pay_card(value_pay)

        self.assertEqual(credit, 1500)
