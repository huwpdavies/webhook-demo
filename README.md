# Webhooks vs polling: live demo

Four small Python programs that show why webhooks beat polling, and how to cope when webhooks go wrong.

| File | Role | Port |
|---|---|---|
| `provider.py` | The payment provider (like Stripe): records payments, answers polls, sends webhooks | 5050 |
| `receiver.py` | Our app receiving webhooks; ignores duplicates | 5001 |
| `poller.py` | Our app polling every 5 seconds instead | none |
| `pay.py` | Triggers a payment, or a duplicate delivery | none |

## One-time setup (macOS/Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `venv\Scripts\activate` and use `python` instead of `python3`.

## Starting the demo

Open **four terminal windows** in this folder. In each one, run `source venv/bin/activate` first.
Start the programs **in this order**, each in its own window:

1. Window 1: `python provider.py`
2. Window 2: `python receiver.py`
3. Window 3: `python poller.py`
4. Window 4: used for commands (`python pay.py`)

Always restart the provider first for a clean run. Restarting wipes its payment list, and the poller and receiver should be restarted after it.

## Commands (window 4)

```bash
python pay.py                  # create one payment
python pay.py resend pay_001   # send the same webhook again (duplicate)
```

## Troubleshooting

- **Address already in use:** an old copy is still running. Stop it with `Ctrl+C`, or find it with `lsof -i :5050`.
- **Poller shows huge delays:** the provider has old payments. Restart provider, receiver and poller.
- **Nothing happens when you run `pay.py`:** check the provider is running in window 1.

The step-by-step talk track is in `DEMO_SCRIPT.md`.
