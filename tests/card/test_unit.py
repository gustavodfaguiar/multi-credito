import unittest
from multi_credit.card.models import Card


class CardUnitModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.card = Card()

    def test_pay_card(self):
        value_pay = 500
        self.card.credit = 1000
        credit = self.card.pay_card(value_pay)

        self.assertEqual(credit, 1500)
