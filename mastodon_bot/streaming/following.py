from mastodon.types import Notification

from mastodon_bot.mastodon_bot.mastodon_bot import BotInterface
from mastodon_bot.mastodon_bot.streaming import CallbackStreamListener


class FollowingHandler(CallbackStreamListener):
    def __init__(self, bot_instance: BotInterface) -> None:
        super().__init__()
        self.__bot = bot_instance
        self.__api = bot_instance.get_api_instance()

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "follow":
            print(f"{notification.account.acct} followed you")

            # Follow back
            # self.__api.account_follow(notification.account.id)
