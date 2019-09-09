from validator.constraints.constraint import Constraint

class Validator():
    def __init__(self, constraints = Constraint()):
        self.constraints = constraints

    def validate(self, account, event):
        if self.constraints is None:
            return []

        return self.constraints.validate(account, event)
