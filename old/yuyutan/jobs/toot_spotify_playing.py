import datetime
import json
import os
from logging import config, getLogger
from pathlib import Path

from dotenv import load_dotenv
from mastodon import Mastodon
from yuyutan.spotify.get_playing import get_playing

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


def toot_spotify_playing() -> None:
    url = get_playing()

    if url is None:
        logger.info("Skipping toot spotify playing")
    else:
        sentence = f"ゆゆ君は今この曲を聞いてるよ\n{url}"
        try:
            api.toot(sentence)
            logger.info(f"Toot: {sentence}")
        except Exception as e:
            logger.error(e)
