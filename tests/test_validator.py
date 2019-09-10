from account.account import Account

from datetime import datetime

from validator.constraints.active_card import ActiveCard
from validator.constraints.constraint import Constraint
from validator.constraints.create_account import CreateAccount
from validator.constraints.doubled_transaction import DoubledTransaction
from validator.constraints.high_frequency_small_interval import HighFrequencySmallInterval
from validator.constraints.insufficient_limit import InsufficientLimit

from validator.validator import Validator

import unittest

class TestValidator(unittest.TestCase):

    def setUp(self):
        self.account = Account()
        self.account.created = True
        self.account.active_card = True
        self.account.available_limit = 100

    def tearDown(self):
        pass

    def test_empty_validator_pass(self):
        account = Account()
        validator = Validator()

        violations = validator.validate(account, {})

        self.assertEqual(violations, [])

    def test_create_account_constraint_pass(self):
        account = Account()
        validator = Validator(CreateAccount())
        event = { "account": { "activeCard": "true", "availableLimit": 100 } }

        violations = validator.validate(account, event)

        self.assertEqual(violations, [])

    def test_create_account_constraint_fail(self):
        validator = Validator(CreateAccount())
        event = { "account": { "activeCard": "true", "availableLimit": 100 } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, ['account-already-initialized'])

    def test_active_card_constraint_pass(self):
        validator = Validator(ActiveCard())
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, [])

    def test_active_card_constraint_fail(self):
        self.account.active_card = False
        validator = Validator(ActiveCard())
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, ['card-not-active'])

    def test_insufficient_limit_constraint_pass(self):
        validator = Validator(InsufficientLimit())
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, [])

    def test_insufficient_limit_constraint_fail(self):
        validator = Validator(InsufficientLimit())
        event = { "transaction": { "merchant": "Burger King", "amount": 101, "time": "2019-09-09T15:52:00.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, ['insufficient_limit'])

    def test_high_frequency_small_interval_constraint_pass(self):
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" })
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:30.000Z" })
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:53:30.000Z" })

        base_time = datetime.strptime('2019-09-09T15:54:30.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")

        validator = Validator(HighFrequencySmallInterval(base_time))
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:54:30.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, [])

    def test_high_frequency_small_interval_constraint_fail(self):
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" })
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:30.000Z" })
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:53:30.000Z" })

        base_time = datetime.strptime('2019-09-09T15:54:00.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")

        validator = Validator(HighFrequencySmallInterval(base_time))
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:54:00.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, ['high_frequency_small_interval'])

    def test_high_doubled_transaction_constraint_pass(self):
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" })
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:53:00.000Z" })

        base_time = datetime.strptime('2019-09-09T15:54:30.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")

        validator = Validator(DoubledTransaction(base_time))
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:54:30.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, [])

    def test_high_doubled_transaction_constraint_fail(self):
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:52:00.000Z" })
        self.account.logs.append({ "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:53:00.000Z" })

        base_time = datetime.strptime('2019-09-09T15:54:00.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")

        validator = Validator(DoubledTransaction(base_time))
        event = { "transaction": { "merchant": "Burger King", "amount": 20, "time": "2019-09-09T15:54:00.000Z" } }

        violations = validator.validate(self.account, event)

        self.assertEqual(violations, ['doubled_transaction'])


if __name__ == '__main__':
    unittest.main()
