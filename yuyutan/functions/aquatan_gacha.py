import logging
import random
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import schedule
from mastodon import Mastodon
from rq_scheduler import Scheduler

from ..mastodon_bot.interfaces.bot import BotInterface
from ..mastodon_bot.interfaces.functions import BotFunctionInterface

logger = logging.getLogger(__name__)


class AquatanGacha(BotFunctionInterface):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler

    def run(self) -> None:
        logger.info("AquatanGacha started.")
        scheduler = schedule.Scheduler()
        scheduler.every(2).days.do(self._enqueue)

        while True:
            scheduler.run_pending()
            time.sleep(1)

    def _enqueue(self) -> None:
        logger.info("Try toot spotify playing...")

        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        delta_hours = random.randint(0, 23)
        delta_minutes = random.randint(0, 59)
        delta_seconds = random.randint(0, 59)
        next_ = now + timedelta(hours=delta_hours, minutes=delta_minutes, seconds=delta_seconds)

        next_jst = datetime(
            next_.year,
            next_.month,
            next_.day,
            next_.hour,
            next_.minute,
            tzinfo=ZoneInfo("Asia/Tokyo"),
        )
        next_utc = next_jst.astimezone(ZoneInfo("UTC"))

        job = self.__scheduler.enqueue_at(next_utc, self._toot, self.__api)
        logger.debug(f"Enqueued at {next_jst}: {job}")

    @staticmethod
    def _toot(api: Mastodon) -> None:
        sentence = "@aquatan ガチャ"
        api.toot(sentence)
