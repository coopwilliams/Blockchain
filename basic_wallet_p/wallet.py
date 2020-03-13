import json
import requests
import sys


if __name__ == "__main__":
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("../client_mining_p/my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    print("""
                               ,--.,--.        ,--.
            ,--.   ,--.,--.,--.|  ||  |,---. ,-'  '-.
            |  |.'.|  ||  ||  ||  ||  | .-. :'-.  .-'
            |   .'.   |'  ''  '|  ||  \   --.  |  |
            '--'   '--' `----' `--'`--'`----'  `--'
            """)

    while True:
        print(f"""\n\n\nWelcome to the wallet, {id}.
        1. Change your ID.
        2. Display your current balance.
        3. Display all your transactions.
        4. Quit.
        """)

        # Take user input
        try:
            choice = int(input("Enter a number: "))
        except:
            continue

        # Change user ID
        if choice == 1:
            id = str(input("Enter a user id"))

        # Get transaction history
        if choice in [2, 3]:
            r = requests.get(url=node + "/chain")
            # Handle non-json response
            try:
                data = r.json()
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(r)
                break

            user_history = []
            for block in data['chain']:
                user_history.extend([t for t in block['transactions']
                                    if id == (t['recipient'] or t['sender'])])
            # Print balance
            if choice == 2:
                balance = sum([t['amount'] for t in user_history if id == t['recipient']]) \
                          - sum([t['amount'] for t in user_history if id == t['sender']])
                print("\n", balance)

            # Print all transaction history
            if choice == 3:
                print("\n---Incoming transactions---")
                for t in user_history:
                    if id == t['recipient']:
                        print("\t", t)
                print("\n---Outgoing transactions---")
                for t in user_history:
                    if id == t['sender']:
                        print("\t", t)

        # Quit
        if choice == 4:
            break
