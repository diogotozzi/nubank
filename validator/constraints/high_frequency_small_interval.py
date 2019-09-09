from datetime import datetime, timedelta
from validator.constraints.abstract_constraint import AbstractConstraint

class HighFrequencySmallInterval(AbstractConstraint):
    def validate(self, account, event):
        if 'transaction' in event:
            latest = datetime.strptime(event['transaction']['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            comparison = datetime.now() - timedelta(minutes = -2)

            if latest > comparison:
                print(str(timestamp))

                return 'high_frequency_small_interval'

        return super().validate(account, event)
