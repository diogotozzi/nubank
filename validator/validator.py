from validator.constraints.constraint import Constraint

class Validator():

    def validate(self, account, event, constraints = None):
        if constraints is None:
            return []

        return constraints.validate(account, event)
