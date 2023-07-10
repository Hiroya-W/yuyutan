import datetime
import json
from pathlib import Path
import markovify
from dotenv import load_dotenv
from mastodon import Mastodon
import os
from logging import getLogger, config

DATA_DIR = Path("datas")
LOG_DIR = Path("logs")


with open(Path("logger_config.json"), "r") as fp:
    logger_config = json.load(fp)

if not LOG_DIR.exists():
    LOG_DIR.mkdir()

logger_config["handlers"]["fileHandler"]["filename"] = (
    LOG_DIR / f"{datetime.datetime.now().isoformat()}.log"
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


def periodic_toot() -> None:
    with open(DATA_DIR / Path("model/model.json"), "r") as fp:
        model_json = fp.read()
    model = markovify.Text.from_json(model_json)

    sentence = model.make_short_sentence(140)
    sentence = "".join(sentence.split(" "))
    try:
        api.toot(sentence)
        logger.info(f"Toot: {sentence}")
    except Exception as e:
        logger.error(e)
