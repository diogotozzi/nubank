from account.account import Account

import fileinput
import json

def main():
    account = Account()

    for line in fileinput.input():
        event = json.loads(line)

main()
