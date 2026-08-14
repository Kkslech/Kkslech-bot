import feedparser
import requests
import json
import os

POSTED_FILE = "posted_links.json"
FEED_URL = "https://kkslech.com/feed/"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHANNEL = os.environ["TELEGRAM_CHANNEL"]

def load_posted():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_posted(links):
    with open(POSTED_FILE, "w") as f:
        json.dump(list(links), f)

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": text
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()

def main():
    posted = load_posted()
    feed = feedparser.parse(FEED_URL)

    new_posted = set(posted)

    for entry in reversed(feed.entries):
        if entry.link not in posted:
            title = entry.title
            text = f"{title}\n{entry.link}"
            send_to_telegram(text)
            new_posted.add(entry.link)
            print(f"Opublikowano: {entry.link}")

    save_posted(new_posted)

if __name__ == "__main__":
    main()
