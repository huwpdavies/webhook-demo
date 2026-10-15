# Build plan: Webhooks vs polling live demo

## Context for Claude Code

I'm a student building a live demo for a 15-minute group presentation on **webhooks vs polling**. I have **2 to 3 hours in total** to build it, test it and rehearse it.

I need two things from this session:

1. **A working demo** I can run live in front of the class.
2. **To understand how it works**, so I can explain every part and answer questions. I'm presenting this, so I can't rely on code I don't follow.

Before writing any code, ask me:
- Which operating system I'm on (Windows, macOS or Linux).
- Whether Python 3 is installed (`python --version` or `python3 --version`).
- How comfortable I am with Python, so you can pitch explanations at the right level.

## How I want you to work with me

- **Explain first, then build.** Before each step, tell me in two or three plain sentences what we're about to build and why it matters for the demo. Then write the code.
- **Small steps.** Build one piece at a time, and stop after each one so I can run it and see it work.
- **I run the commands myself.** Tell me exactly what to type and what I should expect to see. If something fails, help me read the error rather than silently fixing it.
- **Keep the code short and commented.** Each file should be well under 100 lines. Add a comment above each block saying what it does in plain English. Use no clever tricks.
- **Checkpoints.** At the end of each milestone, ask me one or two short questions to check I understood it (see the questions under each milestone). If my answer is off, explain again a different way.
- **Watch the clock.** Each milestone has a time budget. If we're running over, tell me and suggest what to cut. Don't add features I haven't asked for.
- **Use plain language.** When you use a term like "endpoint", "HTTP request" or "idempotent", define it the first time.

## What we're building

Three small Python programs that run at the same time, each in its own terminal window, plus one tiny script to trigger events.

| File | Role in the story | Port |
|---|---|---|
| `provider.py` | The "payment provider" (like Stripe). Records payments, answers polling requests and sends webhooks. | 5050 |
| `receiver.py` | "Our app" receiving webhooks. Reacts the instant a payment arrives and ignores duplicates. | 5001 |
| `poller.py` | "Our app" polling instead. Asks the provider "anything new?" every 5 seconds. | none |
| `pay.py` | Triggers a fake payment, so I don't need to type long `curl` commands live. | none |

**Libraries:** only `flask` and `requests`. Store data in plain Python lists and sets, with no database.

### Behaviour

**`provider.py`**
- `POST /pay` creates a payment with a unique ID (such as `pay_001`), an amount and a timestamp. It then sends a webhook to `http://localhost:5001/webhook` in a background thread, so `/pay` returns at once.
- The webhook sender **retries** if the receiver is down: up to 5 attempts, 3 seconds apart, printing each attempt.
- `GET /payments?after=<last_id>` returns any payments newer than the given ID. It counts every request and prints `poll #N: nothing new` or `poll #N: returned 1 payment`.
- `POST /resend/<payment_id>` sends the same webhook again, to simulate a duplicate delivery.

**`receiver.py`**
- `POST /webhook` receives a payment. It prints `RECEIVED pay_001 after 0.02s` (using the payment's timestamp to work out the delay).
- It keeps a set of payment IDs it has already processed. If the same ID arrives again it prints `DUPLICATE pay_001: ignored`, and still returns 200 so the provider stops retrying.
- It keeps a count of webhooks received.

**`poller.py`**
- Every 5 seconds, it calls `GET /payments?after=<last seen id>`.
- It prints each check with a running tally: `check #12: nothing new (11 wasted, 1 useful)`.
- When it finds a payment, it prints `FOUND pay_001 after 3.8s`.

**`pay.py`**
- Running `python pay.py` creates one payment and prints its ID. Running `python pay.py resend pay_001` triggers a duplicate.

Make the important lines stand out in the terminal, such as RECEIVED, FOUND and DUPLICATE in capitals or colour. Keep the "nothing new" lines quieter.

## Milestones (about 2.5 hours)

### 1. Setup (15 min)
- Create a project folder and a virtual environment, then install `flask` and `requests`.
- Explain what a virtual environment is in one sentence.
- **Done when:** a "hello world" Flask app runs and I can open it in my browser.

### 2. The provider: payments and polling (30 min)
- Build `provider.py` with `POST /pay` and `GET /payments`, without webhooks yet.
- Build `pay.py` to call `/pay`.
- Explain: what an endpoint is, GET vs POST, and what JSON looks like.
- **Done when:** I run `pay.py` and see the payment appear at `http://localhost:5050/payments` in my browser.
- **Check questions:** "What does `/pay` do when it's called?" "Why is `/payments` a GET and `/pay` a POST?"

### 3. The poller (20 min)
- Build `poller.py`.
- Explain: the polling loop, and why the `after` parameter stops it fetching the same payment twice.
- **Done when:** I leave it running for a minute and watch the "wasted" count climb, then trigger a payment and see it found within 5 seconds.
- **Check questions:** "If nothing happens for an hour, how many requests does the poller make?" (720 at 5-second intervals.) "What happens to speed and cost if we poll every 60 seconds instead?"

### 4. Webhooks (30 min)
- Add the webhook sender to `provider.py`, without retries yet. Build `receiver.py`.
- Explain: the direction is reversed (the provider calls us), and why the sender runs in a background thread.
- **Done when:** with all three programs running, one payment shows up in the receiver almost instantly and in the poller a few seconds later.
- **Check questions:** "Why does the receiver need its own URL and port?" "Why does the webhook side make zero requests while nothing happens?"

### 5. Duplicates (15 min)
- Add the processed-IDs set to `receiver.py`, and the `/resend` route and `pay.py resend` option.
- Explain: why real providers sometimes send the same event twice, and what "idempotent" means (handling it twice has the same effect as handling it once).
- **Done when:** resending a payment prints DUPLICATE and nothing else happens.
- **Check question:** "If this were a real shop, what could go wrong without the duplicate check?" (The customer could be charged twice or get two order emails.)

### 6. Missed webhooks and retries (20 min)
- Add the retry loop to the sender.
- Explain: what happens when the receiver is down, and that retries are one fix. Polling occasionally as a back-up "catch-up check" is the other.
- **Done when:** I stop `receiver.py`, trigger a payment, watch the provider print failed attempts, restart the receiver, and see the payment arrive on a retry.
- **Check question:** "What if the receiver is down for longer than all 5 retries?" (The event is lost unless a catch-up poll finds it. This is why real providers retry for days and let you list missed events.)

### 7. Rehearsal kit (20 min)
- Write a short `README.md` with the exact commands to start each program, in order.
- Write a **demo script**: the order of actions for the live demo, with one sentence for me to say at each step (see below).
- Do one full timed run-through with me. The demo slot is about 3 minutes.

## The live demo script (to refine in milestone 7)

1. Start the provider, receiver and poller in three windows side by side. *"Our app can learn about payments in two ways."*
2. Wait 30 seconds. *"Nothing has happened, but the poller has already asked six times. Every one was wasted."*
3. Run `pay.py`. *"The webhook arrived instantly. Polling found it seconds later, after even more requests."*
4. Run `pay.py resend`. *"Providers sometimes send the same event twice. We check the ID and ignore it, so the customer isn't charged twice."*
5. Stop the receiver, run `pay.py`, then restart the receiver. *"If we're down, the provider retries. If it gives up, we need a back-up check."*

## Out of scope (mention on a slide, don't build)

Signature verification, HTTPS, public URLs or tunnelling tools, databases, Docker, a web front end and real payment APIs. If I ask about any of these, explain them briefly but don't add them unless I say so.

## Definition of done

- All four files work, and the full demo script runs from a fresh start in under 3 minutes.
- I can explain, without notes:
  - why polling wastes requests when nothing happens
  - why the webhook arrives faster
  - what the receiver does when a webhook arrives twice
  - what happens when a webhook doesn't arrive at all, and the two ways to recover
- A README lets a groupmate start the demo without my help.
