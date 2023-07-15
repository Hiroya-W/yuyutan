from os import _Environ

from sqlalchemy.orm import Session

from mastodon_bot.mastodon_bot import MastodonBot


class Bot:
    def __init__(self, env: _Environ[str], db: Session) -> None:
        self.__env = env
        self.__db = db
        self.__mastodon_bot = MastodonBot(env=env)

    def run(self) -> None:
        """
        Run the bot
        """
        self.__mastodon_bot.run()
