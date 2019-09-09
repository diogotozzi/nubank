from datetime import datetime, timedelta
from validator.constraints.abstract_constraint import AbstractConstraint

class DoubledTransaction(AbstractConstraint):
    def validate(self, account, event):
        if 'transaction' in event:
            if self.check_violation(event, account.logs) == True:
                return super().validate(account, event) + ['doubled_transaction']

        return super().validate(account, event)

    def check_violation(sefl, event, logs = []):
        counter = 0
        for i in range(0, len(logs)):
            transaction = datetime.strptime(logs[i]['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            comparison = datetime.now() - timedelta(seconds = 120)

            if transaction > comparison:
                if event['transaction']['merchant'] == logs[i]['merchant']:
                    counter += 1

            if i == 1 and counter == 2:
                return True

        return False
