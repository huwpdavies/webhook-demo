# provider.py: the pretend payment provider (like Stripe), on port 5050.
import random
import threading
import time

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Where the provider delivers webhooks: our receiver's URL.
WEBHOOK_URL = "http://localhost:5001/webhook"

# All payments live in a plain list (no database). Newest is last.
payments = []

# How many times someone has asked "anything new?" via /payments.
poll_count = 0


# Retry settings: up to 5 attempts, 3 seconds apart.
MAX_ATTEMPTS = 5
RETRY_DELAY = 3


# Send one payment to the receiver as a POST request (this IS the webhook).
# If the receiver doesn't answer with a success, wait and try again.
def send_webhook(payment):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(WEBHOOK_URL, json=payment, timeout=5)
            if response.ok:  # any 2xx status, such as 200, counts as delivered
                print(f"WEBHOOK SENT {payment['id']} (attempt {attempt})")
                return
            print(f"attempt {attempt}/{MAX_ATTEMPTS} failed: status {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"attempt {attempt}/{MAX_ATTEMPTS} failed: receiver not reachable")

        # Wait before the next try (but not after the last one).
        if attempt < MAX_ATTEMPTS:
            time.sleep(RETRY_DELAY)

    print(f"\033[1;31mWEBHOOK GAVE UP on {payment['id']} after {MAX_ATTEMPTS} attempts\033[0m")


# POST /pay: create a new payment with a unique ID, an amount and a timestamp.
@app.route("/pay", methods=["POST"])
def pay():
    payment = {
        "id": f"pay_{len(payments) + 1:03d}",  # pay_001, pay_002, ...
        "amount": random.choice([10, 25, 40, 99]),
        "timestamp": time.time(),  # seconds since 1970; used later to measure delay
    }
    payments.append(payment)
    print(f"PAYMENT CREATED {payment['id']} (${payment['amount']})")

    # Send the webhook in a background thread so /pay can return immediately.
    threading.Thread(target=send_webhook, args=(payment,)).start()
    return jsonify(payment)


# POST /resend/pay_001: send the same webhook again, to simulate a duplicate delivery.
@app.route("/resend/<payment_id>", methods=["POST"])
def resend(payment_id):
    for payment in payments:
        if payment["id"] == payment_id:
            print(f"RESENDING {payment_id}")
            threading.Thread(target=send_webhook, args=(payment,)).start()
            return jsonify(payment)
    return jsonify({"error": "no such payment"}), 404


# GET /payments?after=pay_002: return every payment newer than that ID.
# With no "after", return all of them.
@app.route("/payments", methods=["GET"])
def list_payments():
    global poll_count
    poll_count += 1

    after = request.args.get("after")
    ids = [p["id"] for p in payments]

    # Find where the "after" payment sits in the list and take everything past it.
    start = ids.index(after) + 1 if after in ids else 0
    new = payments[start:]

    # Keep "nothing new" quiet; make real results stand out.
    if new:
        print(f"poll #{poll_count}: returned {len(new)} payment(s)")
    else:
        print(f"\033[90mpoll #{poll_count}: nothing new\033[0m")
    return jsonify(new)


if __name__ == "__main__":
    app.run(port=5050)
