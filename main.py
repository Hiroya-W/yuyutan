"""
Bot entry point
"""

import os

from dotenv import load_dotenv

from mastodon_bot.core import Bot
from mastodon_bot.databases.mysql import create_session

load_dotenv()


if __name__ == "__main__":
    # DBが変わっても、同じようにSQLAlchemyのSession型で利用できる
    session = create_session(
        username=os.getenv("MYSQL_USERNAME", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database=os.getenv("MYSQL_DATABASE", "mastodon_bot"),
    )

    bot = Bot(
        env=os.environ,
        db=session,
    )

    bot.run()
