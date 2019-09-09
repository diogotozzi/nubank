from validator.constraints.abstract_constraint import AbstractConstraint

class ActiveCard(AbstractConstraint):
    def validate(self, account, event):
        if 'transaction' in event:
            if account.active_card is False:
                return 'card-not-active'

        return super().validate(account, event)
