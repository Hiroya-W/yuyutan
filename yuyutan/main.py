from pathlib import Path
import markovify
from dotenv import load_dotenv
from mastodon import Mastodon
import os

load_dotenv()

api = Mastodon(
    api_base_url=os.environ.get("MASTODON_API_BASE_URL"),
    client_id=os.environ.get("MASTODON_CLIENT_KEY"),
    client_secret=os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token=os.environ.get("MASTODON_ACCESS_TOKEN"),
)


DATA_DIR = Path("datas")


def main() -> None:
    with open(DATA_DIR / Path("model/model.json"), "r") as fp:
        model_json = fp.read()
    model = markovify.Text.from_json(model_json)

    sentence = model.make_short_sentence(140)
    sentence = "".join(sentence.split(" "))
    api.toot(sentence)


if __name__ == "__main__":
    main()
