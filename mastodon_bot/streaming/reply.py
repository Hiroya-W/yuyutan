import logging

from mastodon.types import Notification
from rq_scheduler import Scheduler

from mastodon_bot.mastodon_bot.mastodon_bot import BotInterface
from mastodon_bot.mastodon_bot.streaming import CallbackStreamListener

logger = logging.getLogger(__name__)


class ReplyHandler(CallbackStreamListener):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        super().__init__()
        self.__bot = bot_instance
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "mention":
            logger.info(f"@{notification.account.acct} mentioned you")

            # Reply
            # self.__api.status_post(
            #     f"@{notification.account.acct} Hello!", in_reply_to_id=notification.status.id
            # )
