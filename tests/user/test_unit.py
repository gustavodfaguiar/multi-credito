import unittest
from multi_credit.user.models import User


class UserUnitModelsTestCase(unittest.TestCase):
    def test_small_name_card(self):
        self.user = User("Andre Mendes", "andre@gmail.com", "123456")
        full_name = self.user.name_card

        self.assertEqual(full_name, "ANDRE MENDES")

    def test_middle_name_card(self):
        self.user = User("Isabel Cristina Leopoldina", "isabel@gmail.com", "123456")
        full_name = self.user.name_card

        self.assertEqual(full_name, "ISABEL C LEOPOLDINA")

    def test_big_name_card(self):
        self.user = User("Maria Carmo Miranda da Cunha", "maria@gmail.com", "123456")
        full_name = self.user.name_card

        self.assertEqual(full_name, "MARIA C M CUNHA")
