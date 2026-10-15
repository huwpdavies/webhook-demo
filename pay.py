# pay.py: triggers events on the provider so we don't type long curl commands.
#   python pay.py               -> create one payment
#   python pay.py resend pay_001 -> (added in milestone 5)
import sys

import requests

PROVIDER = "http://localhost:5050"

# Send a POST to /pay and print the payment that comes back.
if len(sys.argv) == 1:
    response = requests.post(f"{PROVIDER}/pay")
    print("Created:", response.json()["id"])
else:
    print("Unknown command (resend arrives in milestone 5)")
