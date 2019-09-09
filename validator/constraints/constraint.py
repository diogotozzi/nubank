from validator.constraints.abstract_constraint import AbstractConstraint

class Constraint(AbstractConstraint):
    def validate(self, account, event):
        return super().validate(account, event)
