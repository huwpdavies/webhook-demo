# Live demo script (about 3 minutes)

## Before you go on

- Four terminals visible: provider, receiver and poller side by side, with a fourth for commands at the bottom.
- Start in order: provider, receiver, poller. Check the poller prints grey "nothing new" lines.
- Pre-type `python pay.py` in window 4 so you only press Enter.
- Increase the terminal font size so the back row can read it.

## Steps

| Time | Action | Say |
|---|---|---|
| 0:00 | Point at the three windows | "Our app can learn about payments in two ways. On the left, the provider. In the middle, webhooks. On the right, polling." |
| 0:15 | Wait about 30 seconds. Point at the poller's wasted count | "Nothing has happened, but the poller has already asked six times. Every one was wasted. The webhook side has made zero requests." |
| 0:50 | Run `python pay.py` | "The webhook arrived instantly. Polling found it seconds later, after even more wasted requests." |
| 1:20 | Run `python pay.py resend pay_001` | "Providers sometimes send the same event twice. We check the ID and ignore it, so the customer doesn't get two emails or two parcels." |
| 1:50 | Ctrl+C the receiver. Run `python pay.py`. Watch the provider's failed attempts. Run `python receiver.py` | "If we're down, the provider retries. If it gives up, we need a back-up check. Polling is a good safety net." |
| 2:40 | Point at RECEIVED, and at the poller finding it | "Webhooks for speed. Polling as the safety net. Most real systems use both." |

## Timing tips

- The provider retries 5 times, 3 seconds apart, so you have about 12 seconds to restart the receiver in the last step. Pre-type `python receiver.py` in that window and press Up then Enter.
- If you're running over, shorten the 30-second wait to 15 seconds. The wasted count still shows.
- If something goes wrong, stop everything and restart in order: provider, receiver, poller.
