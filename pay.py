# pay.py: triggers events on the provider so we don't type long curl commands.
#   python pay.py                 -> create one payment
#   python pay.py resend pay_001  -> make the provider send that webhook again
import sys

import requests

PROVIDER = "http://localhost:5050"

# No arguments: send a POST to /pay and print the ID that comes back.
if len(sys.argv) == 1:
    response = requests.post(f"{PROVIDER}/pay")
    print("Created:", response.json()["id"])

# "resend <id>": ask the provider to deliver that webhook a second time.
elif len(sys.argv) == 3 and sys.argv[1] == "resend":
    response = requests.post(f"{PROVIDER}/resend/{sys.argv[2]}")
    print("Resent:" if response.ok else "Failed:", sys.argv[2])

else:
    print("Usage: python pay.py   or   python pay.py resend pay_001")
