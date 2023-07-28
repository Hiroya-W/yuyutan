import logging
import time
from datetime import timedelta
from pathlib import Path

from mastodon import Mastodon
from rq_scheduler import Scheduler

from ..markov_chain import MarkovChain
from ..mastodon_bot.interfaces.bot import BotInterface
from ..mastodon_bot.interfaces.functions import BotFunctionInterface

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "datas"
MODEL_DIR = DATA_DIR / "model"


class PeriodicToot(BotFunctionInterface):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler
        self.__markov_chain = MarkovChain(MODEL_DIR / "model.json")

    def run(self) -> None:
        logger.info("Periodic toot started.")
        while True:
            sentence = self.__markov_chain.make_short_sentence(140)
            logger.info(f"Periodic toot: {sentence}")
            self.__scheduler.enqueue_in(
                timedelta(seconds=5), self.__toot, self.__api, sentence
            )
            time.sleep(60)

    @staticmethod
    def __toot(api: Mastodon, sentence: str) -> None:
        # api.toot(sentence)
        pass
