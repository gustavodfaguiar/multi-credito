from multi_credit import app, db
import unittest
from multi_credit.wallet.models import Wallet
from multi_credit.user.models import User


class WalletUnitModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.from_object('multi_credit.config.TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_create_wallet(self):
        with self.app.app_context():
            wallet = Wallet().create_wallet(1)
            self.assertEqual(wallet, True)

    def test_create_wallet_that_already_exists(self):
        with self.app.app_context():
            wallet = Wallet().create_wallet(1)
            wallet = Wallet().create_wallet(1)
            self.assertEqual(wallet, False)
