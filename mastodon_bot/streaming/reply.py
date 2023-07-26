import logging
from datetime import timedelta

from mastodon import Mastodon
from mastodon.types import Notification
from rq_scheduler import Scheduler

from mastodon_bot.mastodon_bot.interfaces.bot import BotInterface
from mastodon_bot.mastodon_bot.interfaces.streaming import (
    CallbackStreamListener,
)

logger = logging.getLogger(__name__)


class ReplyHandler(CallbackStreamListener):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        super().__init__()
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "mention":
            logger.info(f"@{notification.account.acct} mentioned you")
            self.__scheduler.enqueue_in(
                timedelta(seconds=5), self.__reply, self.__api, notification
            )

    @staticmethod
    def __reply(api: Mastodon, notification: Notification) -> None:
        # api.status_post(
        #     f"@{notification.account.acct} Hello!", in_reply_to_id=notification.status.id
        # )
        pass
