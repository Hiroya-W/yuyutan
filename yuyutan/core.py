import logging
import time
from os import _Environ

from redis import Redis
from rq_scheduler import Scheduler
from sqlalchemy.orm import Session

from yuyutan.functions import AquatanGacha, PeriodicToot, TryTootSpotifyPlaying
from yuyutan.mastodon_bot import MastodonBot
from yuyutan.streaming import FollowingHandler, ReplyHandler

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, env: _Environ[str], db: Session, redis: Redis) -> None:
        self.__env = env
        # DatabaseはSQLAlchemynを使って差し替えが可能
        self.__db = db
        # Redisはfakeredis-pyを使って差し替えが可能
        self.__redis = redis
        # 各ハンドラ内のスケジューリングに使う
        # できれば、引数で渡すのではなく、処理を透過的にスケジューリングできるようにしたい
        self.__scheduler = Scheduler(connection=self.__redis)
        self.__mastodon_bot = MastodonBot(env=env)
        self.__mastodon_bot.add_listeners(
            [
                FollowingHandler(self.__mastodon_bot, self.__scheduler),
                ReplyHandler(self.__mastodon_bot, self.__scheduler),
            ]
        )
        # ここで登録された関数はそれぞれ別スレッド上で実行される
        self.__mastodon_bot.add_functions(
            [
                PeriodicToot(self.__mastodon_bot, self.__scheduler),
                TryTootSpotifyPlaying(self.__mastodon_bot, self.__scheduler),
                AquatanGacha(self.__mastodon_bot, self.__scheduler),
            ]
        )
        logger.debug("Bot initialized.")

    def run(self) -> None:
        """
        Run the bot
        """

        logger.info("Bot started.")
        self.__mastodon_bot.run()
        while True:
            time.sleep(1)
