import datetime
import json
import os
from logging import config, getLogger
from pathlib import Path

from dotenv import load_dotenv
from mastodon import Mastodon, streaming
from mastodon.types import Notification

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


def notification_handler(notification: Notification) -> None:
    if notification.type == "follow":
        account_id = notification.account.id
        username = notification.account.username
        display_name = notification.account.display_name
        try:
            api.account_follow(
                id=account_id
            )
            api.toot(
                f"@{username} {display_name}、フォローありがとうっちゃ！"
            )

            logger.info(f"follow {display_name}")
        except Exception as e:
            logger.error(e)


listener = streaming.CallbackStreamListener(
    notification_handler=notification_handler
)

api.stream_user(
    listener=listener,
    run_async=True,
    reconnect_async=True
)


if __name__ == "__main__":
    while True:
        pass
