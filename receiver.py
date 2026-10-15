# receiver.py: "our app" receiving webhooks, on port 5001.
import time

from flask import Flask, request

app = Flask(__name__)

# How many webhooks have arrived.
received_count = 0

# IDs of payments we've already processed. A set can't hold the same ID twice.
processed_ids = set()


# POST /webhook: the provider calls this the moment a payment happens.
@app.route("/webhook", methods=["POST"])
def webhook():
    global received_count
    payment = request.get_json()  # the payment, sent as JSON in the request body

    # Seen this ID before? Ignore it, but still reply 200 so the provider stops retrying.
    if payment["id"] in processed_ids:
        print(f"\033[1;33mDUPLICATE {payment['id']}: ignored\033[0m")
        return "", 200

    processed_ids.add(payment["id"])
    received_count += 1

    # Delay = now minus the moment the provider created the payment.
    delay = time.time() - payment["timestamp"]
    print(f"\033[1;36mRECEIVED {payment['id']} after {delay:.2f}s "
          f"(webhook #{received_count})\033[0m")

    # Reply 200 ("OK") so the provider knows we got it.
    return "", 200


if __name__ == "__main__":
    app.run(port=5001)
