from abc import ABC, abstractmethod

class AbstractConstraint(ABC):
    def __init__(self):
        self._next_validation = None

    def set_next(self, validation):
        self._next_validation = validation
        return validation

    @abstractmethod
    def validate(self, account, event):
        if self._next_validation:
            return self._next_validation.validate(account, event)

        return []
