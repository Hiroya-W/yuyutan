import time
from os import _Environ

from sqlalchemy.orm import Session

from mastodon_bot.mastodon_bot import MastodonBot
from mastodon_bot.streaming import FollowingHandler, ReplyHandler


class Bot:
    def __init__(self, env: _Environ[str], db: Session) -> None:
        self.__env = env
        self.__db = db
        self.__mastodon_bot = MastodonBot(env=env)
        self.__mastodon_bot.add_listener_many(
            [
                FollowingHandler(),
                ReplyHandler(),
            ]
        )

    def run(self) -> None:
        """
        Run the bot
        """

        self.__mastodon_bot.run()
        while True:
            time.sleep(1)
