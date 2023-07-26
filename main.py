"""
Bot entry point
"""

import logging
import logging.config
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from redis import Redis

from mastodon_bot.core import Bot
from mastodon_bot.databases.mysql import create_session

load_dotenv()

logging_file = Path("logging.yaml")
with open(logging_file, "r") as f:
    logging_config = yaml.safe_load(f)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # DBが変わっても、同じようにSQLAlchemyのSession型で利用できる
    session = create_session(
        username=os.getenv("MYSQL_USERNAME", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database=os.getenv("MYSQL_DATABASE", "mastodon_bot"),
    )
    # Redisはfakeredis-pyを使って差し替える
    redis = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=os.getenv("REDIS_PORT", 6379),
    )

    logger.debug("Bot initializing...")
    bot = Bot(env=os.environ, db=session, redis=redis)

    logger.info("Bot starting...")
    bot.run()
