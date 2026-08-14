import feedparser
import tweepy
import json
import os

POSTED_FILE = "posted_links.json"
FEED_URL = "https://kkslech.com/feed/"

def load_posted():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_posted(links):
    with open(POSTED_FILE, "w") as f:
        json.dump(list(links), f)

def main():
    posted = load_posted()
    feed = feedparser.parse(FEED_URL)

    client = tweepy.Client(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
    )

    new_posted = set(posted)

    for entry in reversed(feed.entries):
        if entry.link not in posted:
            title = entry.title
            text = f"{title}\n{entry.link}"
            client.create_tweet(text=text)
            new_posted.add(entry.link)
            print(f"Opublikowano: {entry.link}")

    save_posted(new_posted)

if __name__ == "__main__":
    main()
