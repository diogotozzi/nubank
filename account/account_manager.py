from account.account import Account
from validator.validator import Validator

class AccountManager():
    def __init__(self):
        self.accounts = {}

    def events(self, event = {}):
        self.event = event
        return self

    def validations(self, validator = Validator()):
        self.validator = validator
        return self

    def process(self):
        if 'account' in self.event:
            account, violations = self.process_creation(self.event['account'])

        if 'transaction' in self.event:
            account, violations = self.process_transaction(self.event['transaction'])

        return {'account': {'activeCard': account.active_card, 'availableLimit': account.available_limit}, 'violations': violations}

    def process_creation(self, event):
        id = event['id']

        violations = []
        if self.account_exists(id):
            violations = self.validator.validate(self.accounts[id], self.event)
            return self.accounts[id], violations

        account = Account()

        account.created = True
        account.id = event['id']
        account.active_card = event['activeCard']
        account.available_limit = event['availableLimit']

        self.accounts[id] = account

        return account, violations

    def process_transaction(self, event):
        id = event['id']

        if not self.account_exists(id):
            return Account(), ['account-doesnt-exist']

        violations = self.validator.validate(self.accounts[id], self.event)

        self.accounts[id].available_limit -= event['amount']
        self.accounts[id].logs.append({'merchant': event['merchant'], 'time': event['time']})

        return self.accounts[id], violations

    def account_exists(self, id = 0):
        if id in self.accounts:
            return True

        return False
