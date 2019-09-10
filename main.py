from account.account_manager import AccountManager

from validator.constraints.active_card import ActiveCard
from validator.constraints.constraint import Constraint
from validator.constraints.create_account import CreateAccount
from validator.constraints.doubled_transaction import DoubledTransaction
from validator.constraints.high_frequency_small_interval import HighFrequencySmallInterval
from validator.constraints.insufficient_limit import InsufficientLimit

from validator.validator import Validator

import fileinput
import json

def main():
    accountmanager = AccountManager()

    constraints = Constraint()
    constraints \
        .set_next(CreateAccount()) \
        .set_next(ActiveCard()) \
        .set_next(InsufficientLimit()) \
        .set_next(HighFrequencySmallInterval()) \
        .set_next(DoubledTransaction()) \

    validator = Validator(constraints)

    for line in fileinput.input():
        event = json.loads(line)

        accountmanager.events(event).validations(validator)
        result = accountmanager.process()

        print(json.dumps(result))

main()
