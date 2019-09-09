from validator.constraints.abstract_constraint import AbstractConstraint

class InsufficientLimit(AbstractConstraint):
    def validate(self, account, event):
        if 'transaction' in event:
            if account.available_limit < event['transaction']['amount']:
                return 'insufficient_limit'

        return super().validate(account, event)
