from datetime import datetime, timedelta
from validator.constraints.abstract_constraint import AbstractConstraint

class DoubledTransaction(AbstractConstraint):
    def __init__(self, base_time = datetime.now(), seconds = 120):
        super().__init__()
        self.base_time = base_time
        self.seconds = seconds

    def validate(self, account, event):
        if 'transaction' in event:
            if self.check_violation(event, account.logs):
                return super().validate(account, event) + ['doubled_transaction']

        return super().validate(account, event)

    def check_violation(self, event, logs = []):
        counter = 0
        for i in range(0, len(logs)):
            transaction = datetime.strptime(logs[i]['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            comparison = self.base_time - timedelta(seconds = self.seconds)

            if transaction > comparison:
                if event['transaction']['merchant'] == logs[i]['merchant']:
                    counter += 1

            if i == 1 and counter == 2:
                return True

        return False
