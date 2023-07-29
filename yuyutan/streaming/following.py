import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from mastodon import Mastodon
from mastodon.types import Notification
from rq_scheduler import Scheduler

from ..mastodon_bot.interfaces.bot import BotInterface
from ..mastodon_bot.interfaces.streaming import CallbackStreamListener

logger = logging.getLogger(__name__)


class FollowingHandler(CallbackStreamListener):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        super().__init__()
        # BotInterfaceで抽象化されているように見えて、
        # 実際には具象クラスのMastodonを利用しているのであまり意味がない気がする
        # Mastodonのように振る舞うクラスを返せるようになれば嬉しい？
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "follow":
            logger.info(f"@{notification.account.acct} followed you")
            next_ = timedelta(seconds=5)
            job = self.__scheduler.enqueue_in(
                next_, self._follow_back, self.__api, notification
            )
            logger.debug(
                f"Enqueued at {datetime.now(tz=ZoneInfo('Asia/Tokyo')) + next_}: {job}"
            )

    @staticmethod
    def _follow_back(api: Mastodon, notification: Notification) -> None:
        api.account_follow(notification.account.id)
