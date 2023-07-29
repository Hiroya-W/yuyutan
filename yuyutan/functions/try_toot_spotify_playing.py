import logging
import random
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import schedule
from mastodon import Mastodon
from rq_scheduler import Scheduler

from yuyutan.spotify.get_playing import get_playing

from ..mastodon_bot.interfaces.bot import BotInterface
from ..mastodon_bot.interfaces.functions import BotFunctionInterface

logger = logging.getLogger(__name__)


class TryTootSpotifyPlaying(BotFunctionInterface):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler

    def run(self) -> None:
        logger.info("TryTootSpotifyPlaying started.")
        # scheduleを使うのをやめて、cronみたいに書きたい
        schedule.every(4).hours.do(self._enqueue)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def _enqueue(self) -> None:
        logger.info("Try toot spotify playing...")

        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        delta_hours = random.randint(1, 4)
        next_ = now + timedelta(hours=delta_hours)

        next_minutes = random.randint(0, 59)

        next_ = datetime(
            next_.year,
            next_.month,
            next_.day,
            next_.hour,
            next_minutes,
            tzinfo=ZoneInfo("Asia/Tokyo"),
        ).astimezone(ZoneInfo("UTC"))

        self.__scheduler.enqueue_at(next_, self._toot, self.__api)

    @staticmethod
    def _toot(api: Mastodon) -> None:
        url = get_playing()

        if url is None:
            # 何も聞いていない場合は何もしない
            # loggerを使いたいけど、RQ Workerからloggerを使えない...
            return

        sentence = f"ゆゆ君は今この曲を聞いてるよ\n{url}"
        api.toot(sentence)
