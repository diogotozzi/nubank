from account.account import Account

from validator.constraints.active_card import ActiveCard
from validator.constraints.constraint import Constraint
from validator.constraints.create_account import CreateAccount
from validator.constraints.high_frequency_small_interval import HighFrequencySmallInterval
from validator.constraints.insufficient_limit import InsufficientLimit

from validator.validator import Validator

import fileinput
import json

def main():
    account = Account()

    validator = Validator()

    constraints = Constraint()
    constraints.set_next(CreateAccount()).set_next(ActiveCard()).set_next(InsufficientLimit()).set_next(HighFrequencySmallInterval())

    for line in fileinput.input():
        event = json.loads(line)

main()
