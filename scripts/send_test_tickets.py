import argparse
import json
import urllib.error
import urllib.request

TICKETS = [
    ("T-1001", "Aisha", "My card was stolen and I see payments I did not make"),
    ("T-1002", "Rahim", "Why was I charged twice for the same purchase?"),
    ("T-1003", "Nusrat", "How do I top up my account?"),
    ("T-1004", "Karim", "I still haven't received my card, where is it?"),
    ("T-1005", "Mina", "What is the exchange rate for US dollars?"),
    ("T-1006", "Tanvir", "My transfer is still pending after two days"),
    ("T-1007", "Lina", "blah blah something completely random"),
    ("T-1008", "Sabbir", "hi"),
    ("T-1009", "Farhan", "I forgot my passcode and cannot log in"),
]


def send(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") or "{}"
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"raw": body}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="use the n8n test webhook (click 'Execute workflow' in n8n first)")
    parser.add_argument("--host", default="http://localhost:5678")
    args = parser.parse_args()
    url = f"{args.host}/{'webhook-test' if args.test else 'webhook'}/ticket"
    print("POST", url, "\n")

    for ticket_id, customer, text in TICKETS:
        status, res = send(url, {"ticket_id": ticket_id, "customer": customer, "text": text})
        if status == 200:
            print(f"{ticket_id} | {status} | {res.get('priority', '?'):<6} | route={res.get('route', '?'):<12} | "
                  f"{res.get('intent', '?'):<28} | conf={res.get('confidence')} | alerted={res.get('alerted')}")
        else:
            print(f"{ticket_id} | {status} | {res}")


if __name__ == "__main__":
    main()
