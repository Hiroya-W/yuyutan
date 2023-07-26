import logging
import time
from datetime import timedelta

from mastodon import Mastodon
from rq_scheduler import Scheduler

from ..mastodon_bot.interfaces.bot import BotInterface
from ..mastodon_bot.interfaces.functions import BotFunctionInterface

logger = logging.getLogger(__name__)


class PeriodicToot(BotFunctionInterface):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler

    def run(self) -> None:
        while True:
            sentence = "Hello, world!"
            logger.info(f"Periodic toot: {sentence}")
            self.__scheduler.enqueue_in(
                timedelta(seconds=5), self.__toot, self.__api, sentence
            )
            time.sleep(60)

    @staticmethod
    def __toot(api: Mastodon, sentence: str) -> None:
        # api.toot(sentence)
        pass
