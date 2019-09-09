from validator.constraints.abstract_constraint import AbstractConstraint

class CreateAccount(AbstractConstraint):
    def validate(self, account, event):
        if 'account' in event:
            if account.created is True:
                return 'account-already-initialized'

        return super().validate(account, event)
