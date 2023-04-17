import json
import re
from pathlib import Path
import sqlite3

DATA_DIR = Path("datas")
TWEETS_FILE_PATH = DATA_DIR / Path("twitter/data/tweets.js")

search_patterns = ["^RT", "https", "http", "@Youtube"]
replypattern = r"@\w+\s?"


def contains_keywords(text: str, search_patterns: list[str]) -> bool:
    for pattern in search_patterns:
        if re.search(pattern, text):
            return True

    return False


def get_all() -> list[str]:
    with open(TWEETS_FILE_PATH) as fp:
        tweets_js = fp.read()

    tweets_json = json.loads(tweets_js[tweets_js.find("[") :])

    tweets = []
    for tweet in tweets_json:
        full_text = tweet["tweet"]["full_text"]
        tweets.append(full_text)

    return tweets


def main() -> None:
    dbname = DATA_DIR / Path("twitter/tweets.db")
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS tweets")
    cur.execute(
        """
            CREATE TABLE tweets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet STRING
            )
        """
    )

    tweets = get_all()
    filtered_tweets: list[tuple[str]] = []

    for tweet in tweets:
        if contains_keywords(tweet, search_patterns):
            continue

        # リプライのメンションを取り除く
        preprocessed_text = re.sub(replypattern, "", tweet)
        # ハッシュタグを取り除く
        preprocessed_text = re.sub(r"#\w+\s?", "", preprocessed_text)
        # 改行前と後にある空白を取り除く
        splitted_texts = preprocessed_text.lstrip().rstrip().split("\n")

        for splitted_text in splitted_texts:
            filtered_tweets.append((splitted_text,))

    cur.executemany("INSERT INTO tweets(tweet) VALUES (?)", filtered_tweets)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
