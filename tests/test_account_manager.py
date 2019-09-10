from account.account import Account
from account.account_manager import AccountManager

from validator.constraints.active_card import ActiveCard
from validator.constraints.constraint import Constraint
from validator.constraints.create_account import CreateAccount
from validator.constraints.doubled_transaction import DoubledTransaction
from validator.constraints.high_frequency_small_interval import HighFrequencySmallInterval
from validator.constraints.insufficient_limit import InsufficientLimit

from validator.validator import Validator

import unittest

class TestAccountManager(unittest.TestCase):

    def setUp(self):
        self.account = Account()
        self.accountmanager = AccountManager(self.account)

        self.constraints = Constraint()
        self.constraints \
            .set_next(CreateAccount()) \
            .set_next(ActiveCard()) \
            .set_next(InsufficientLimit()) \
            .set_next(HighFrequencySmallInterval()) \
            .set_next(DoubledTransaction()) \

    def tearDown(self):
        pass

    def test_accountmanager_create_account_pass(self):
        event = { "account": { "activeCard": "true", "availableLimit": 100 } }
        self.accountmanager.events(event).validations(Validator(self.constraints))

        self.assertEqual(self.accountmanager.process(), {'account': {'activeCard': True, 'availableLimit': 100}, 'violations': []})

    def test_accountmanager_create_account_fail(self):
        self.account.created = True
        self.account.active_card = True
        self.account.available_limit = 100

        event = { "account": { "activeCard": "true", "availableLimit": 100 } }
        self.accountmanager.events(event).validations(Validator(self.constraints))

        self.assertEqual(self.accountmanager.process(), {'account': {'activeCard': True, 'availableLimit': 100}, 'violations': ['account-already-initialized']})

    def test_accountmanager_create_account_no_active_card_pass(self):
        event = { "account": { "activeCard": "false", "availableLimit": 100 } }
        self.accountmanager.events(event).validations(Validator(self.constraints))

        self.assertEqual(self.accountmanager.process(), {'account': {'activeCard': False, 'availableLimit': 100}, 'violations': []})

    def test_accountmanager_create_account_wrong_parameters(self):
        event = { "accountt": { "activeCardd": "falsee", "availableLimitt": 100 } }
        self.accountmanager.events(event).validations(Validator(self.constraints))

        self.assertEqual(self.accountmanager.process(), {'account': {'activeCard': False, 'availableLimit': 0}, 'violations': []})

    def test_accountmanager_transaction_pass(self):
        event = { "account": { "activeCard": "true", "availableLimit": 100 } }
        self.accountmanager.events(event).validations(Validator(self.constraints))
        self.accountmanager.process()

        event = { "transaction": { "merchant": "Burger King", "amount": 10, "time": "2019-09-09T15:52:00.000Z" } }
        self.accountmanager.events(event).validations(Validator(self.constraints))

        self.assertEqual(self.accountmanager.process(), {'account': {'activeCard': True, 'availableLimit': 90}, 'violations': []})

    def test_accountmanager_transaction_wrong_parameters(self):
        event = { "account": { "activeCard": "true", "availableLimit": 100 } }
        self.accountmanager.events(event).validations(Validator(self.constraints))
        self.accountmanager.process()

        event = { "transactionn": { "merchantt": "Burger King", "amountt": 10, "timee": "2019-09-09T15:52:00.000Z" } }
        self.accountmanager.events(event).validations(Validator(self.constraints))

        self.assertEqual(self.accountmanager.process(), {'account': {'activeCard': True, 'availableLimit': 100}, 'violations': []})

if __name__ == '__main__':
    unittest.main()
