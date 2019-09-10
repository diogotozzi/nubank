from account.account import Account
from validator.validator import Validator

class AccountManager():
    def __init__(self, account = Account()):
        self.account = account

    def events(self, event = {}):
        self.event = event
        return self

    def validations(self, validator = Validator()):
        self.validator = validator
        return self

    def process(self):
        violations = self.validator.validate(self.account, self.event)

        if not violations:
            if 'account' in self.event:
                self.process_creation(self.event['account'])

            if 'transaction' in self.event:
                self.process_transaction(self.event['transaction'])

        return {'account': {'activeCard': self.account.active_card, 'availableLimit': self.account.available_limit}, 'violations': violations}

    def process_creation(self, event):
        self.account.created = True
        self.account.active_card = 'true' in event['activeCard'] or False
        self.account.available_limit = event['availableLimit']

    def process_transaction(self, event):
        self.account.available_limit -= event['amount']
        self.account.logs.append({'merchant': event['merchant'], 'time': event['time']})
