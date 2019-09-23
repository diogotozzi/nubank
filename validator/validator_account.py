from validator.constraints.constraint import Constraint

class ValidatorAccount():
    def __init__(self, constraints = Constraint()):
        self.constraints = constraints

    def validate(self, accounts, event):
        if self.constraints is None:
            return []

        return self.constraints.validate(accounts, event)
