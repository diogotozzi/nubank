class Account():
    def __init__(self):
        self.created = False
        self.active_card = False
        self.available_limit = 0
        self.logs = []

    def process(self, event):
        if 'account' in event:
            self.process_creation(event['account'])

        if 'transaction' in event:
            self.process_transaction(event['transaction'])

    def process_creation(self, event):
        self.created = True
        self.active_card = event['activeCard']
        self.available_limit = event['availableLimit']

    def process_transaction(self, event):
        self.available_limit -= event['amount']
        self.logs.append({'merchant': event['merchant'], 'time': event['time']})
