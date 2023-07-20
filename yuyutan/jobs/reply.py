import datetime
import json
import os
from logging import config, getLogger
from pathlib import Path

import markovify
from dotenv import load_dotenv
from mastodon import Mastodon
from mastodon.types import Account
import random
from spacy.lang.ja import Japanese

DATA_DIR = Path("datas")
LOG_DIR = Path("logs")


with open(Path("logger_config.json"), "r") as fp:
    logger_config = json.load(fp)

if not LOG_DIR.exists():
    LOG_DIR.mkdir()

logger_config["handlers"]["fileHandler"]["filename"] = (
    LOG_DIR / f"{datetime.datetime.now().isoformat()}-{Path(__file__).name}.log"
)

config.dictConfig(logger_config)
logger = getLogger(__name__)


load_dotenv()

api = Mastodon(
    api_base_url=os.environ.get("MASTODON_API_BASE_URL"),
    client_id=os.environ.get("MASTODON_CLIENT_KEY"),
    client_secret=os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token=os.environ.get("MASTODON_ACCESS_TOKEN"),
)


def reply(reply_to_id: str, from_account: Account, content: str) -> None:
    with open(DATA_DIR / Path("model/model.json"), "r") as fp:
        model_json = fp.read()
    model = markovify.Text.from_json(model_json)

    nlp = Japanese()
    doc = nlp(content)

    candidates = []

    for word in nlp(doc):
        if word.pos_ in ["ADV", "NOUN", "ADJ", "VERB"]:
            try:
                sentence = model.make_sentence_with_start(beginning=word.text)
                sentence = "".join(sentence.split(" "))
                if len(sentence) < 140:
                    candidates.append(sentence)
            except Exception as e:
                print(e)

    if candidates == []:
        candidates.append(
            model.make_short_sentence(140)
        )

    random.shuffle(candidates)
    sentence = candidates[0]

    reply_str = f"@{from_account.username} {sentence}"
    try:
        api.status_post(
            reply_str,
            in_reply_to_id=reply_to_id
        )
        logger.info(f"Reply: {reply_str}")
    except Exception as e:
        logger.error(e)
