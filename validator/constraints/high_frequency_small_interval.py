from datetime import datetime, timedelta
from validator.constraints.abstract_constraint import AbstractConstraint

class HighFrequencySmallInterval(AbstractConstraint):
    def validate(self, account, event):
        if 'transaction' in event:
            if self.check_violation(account.logs) == True:
                return 'high_frequency_small_interval'

        return super().validate(account, event)

    def check_violation(sefl, logs = []):
        counter = 0
        for i in range(0, len(logs)):
            transaction = datetime.strptime(logs[i]['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            comparison = datetime.now() - timedelta(seconds = 120)

            if transaction > comparison:
                counter += 1

            if i == 2 and counter == 3:
                return True

        return False
