from validator.constraints.constraint import Constraint

class Validator():

    def validate(self, account, event, constraints = None):
        if constraints is None:
            return None

        return constraints.validate(account, event)
