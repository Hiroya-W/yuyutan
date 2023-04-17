import json
from pathlib import Path
import pandas as pd

DATA_DIR = Path("datas")
TWEETS_FILE_PATH = DATA_DIR / Path("twitter/data/tweets.js")


def main() -> None:
    with open(TWEETS_FILE_PATH) as fp:
        tweets_js = fp.read()

    tweets_json = json.loads(tweets_js[tweets_js.find("[") :])

    cols = ["created_at", "full_text"]
    tweets_df = pd.DataFrame(index=[], columns=cols)

    for tweet in tweets_json:
        created_at = tweet["tweet"]["created_at"]
        full_text = tweet["tweet"]["full_text"]
        tweet_series = pd.Series([created_at, full_text], index=tweets_df.columns)
        tweets_df = pd.concat(
            [tweets_df, pd.DataFrame([tweet_series])], ignore_index=True
        )

    print(tweets_df.head())


if __name__ == "__main__":
    main()
