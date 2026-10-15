# poller.py: "our app" learning about payments by polling (asking repeatedly).
import time

import requests

PROVIDER = "http://localhost:5050"
INTERVAL = 5  # seconds between checks

# The ID of the newest payment we've seen. None means "we've seen nothing yet".
last_id = None

# Running tally of checks.
checks = 0
useful = 0

print(f"Polling {PROVIDER} every {INTERVAL}s. Ctrl+C to stop.")

# Loop forever: ask, report, sleep, repeat.
while True:
    checks += 1

    # Ask the provider for anything newer than the last payment we saw.
    params = {"after": last_id} if last_id else {}
    new_payments = requests.get(f"{PROVIDER}/payments", params=params).json()

    if new_payments:
        useful += 1
        for p in new_payments:
            # Delay = now minus the moment the provider created the payment.
            delay = time.time() - p["timestamp"]
            print(f"\033[1;32mFOUND {p['id']} after {delay:.1f}s\033[0m")
            last_id = p["id"]  # remember it so we never fetch it again
    else:
        wasted = checks - useful
        print(f"\033[90mcheck #{checks}: nothing new ({wasted} wasted, {useful} useful)\033[0m")

    time.sleep(INTERVAL)
