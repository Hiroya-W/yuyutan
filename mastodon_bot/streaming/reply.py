from mastodon.types import Notification

from mastodon_bot.mastodon_bot.mastodon_bot import BotInterface
from mastodon_bot.mastodon_bot.streaming import CallbackStreamListener


class ReplyHandler(CallbackStreamListener):
    def __init__(self, bot_instance: BotInterface) -> None:
        super().__init__()
        self.__bot = bot_instance
        self.__api = bot_instance.get_api_instance()

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "mention":
            print(f"{notification.account.acct} mentioned you")

            # Reply
            # self.__api.status_post(
            #     f"@{notification.account.acct} Hello!", in_reply_to_id=notification.status.id
            # )
