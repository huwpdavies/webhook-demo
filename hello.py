# A minimal Flask app, just to prove our setup works.
from flask import Flask

# Create the web app.
app = Flask(__name__)


# When a browser asks for "/", send back this text.
@app.route("/")
def hello():
    return "Hello, webhooks!"


# Start the server on port 5050 (the port provider.py will use later).
# We avoid 5000 because macOS AirPlay Receiver uses it.
if __name__ == "__main__":
    app.run(port=5050)
