from datetime import datetime, timedelta
from validator.constraints.abstract_constraint import AbstractConstraint

class HighFrequencySmallInterval(AbstractConstraint):
    def __init__(self, base_time = datetime.now(), seconds = 120):
        super().__init__()
        self.base_time = base_time
        self.seconds = seconds

    def validate(self, account, event):
        if 'transaction' in event:
            if self.check_violation(account.logs):
                return super().validate(account, event) + ['high_frequency_small_interval']

        return super().validate(account, event)

    def check_violation(self, logs = []):
        counter = 0
        for i in range(0, len(logs)):
            transaction = datetime.strptime(logs[i]['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            comparison = self.base_time - timedelta(seconds = self.seconds)

            if transaction > comparison:
                counter += 1

            if i == 2 and counter == 3:
                return True

        return False
