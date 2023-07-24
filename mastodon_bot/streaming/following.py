import logging
from datetime import timedelta

from mastodon import Mastodon
from mastodon.types import Notification
from rq_scheduler import Scheduler

from mastodon_bot.mastodon_bot.mastodon_bot import BotInterface
from mastodon_bot.mastodon_bot.streaming import CallbackStreamListener

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
            self.__scheduler.enqueue_in(
                timedelta(seconds=5), self.__follow_back, self.__api, notification
            )

    @staticmethod
    def __follow_back(api: Mastodon, notification: Notification) -> None:
        # api.account_follow(notification.account.id)
        pass
