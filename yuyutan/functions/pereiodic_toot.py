import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import schedule
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
        # scheduleを使うのをやめて、cronみたいに書きたい
        # run()はスレッド上で動かすので、schedulerはここで作る
        # https://teratail.com/questions/182785
        scheduler = schedule.Scheduler()
        scheduler.every(60).minutes.do(self._enqueue)

        while True:
            scheduler.run_pending()
            time.sleep(1)

    def _enqueue(self) -> None:
        sentence = self.__markov_chain.make_short_sentence(140)
        logger.info(f"Periodic toot: {sentence}")

        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        # 今の時間から次に0分になる時間
        # ちゃんと日付もまたいでくれる
        next_ = now + timedelta(hours=1)

        # ちょうど0分に投稿
        next_jst = datetime(
            next_.year,
            next_.month,
            next_.day,
            next_.hour,
            0,
            tzinfo=ZoneInfo("Asia/Tokyo"),
        )
        next_utc = next_jst.astimezone(ZoneInfo("UTC"))  # rq-schedulerはUTCにしないといけない

        job = self.__scheduler.enqueue_at(next_utc, self._toot, self.__api, sentence)
        logger.debug(f"Enqueued at {next_jst}: {job}")

    @staticmethod
    def _toot(api: Mastodon, sentence: str) -> None:
        api.toot(sentence)
