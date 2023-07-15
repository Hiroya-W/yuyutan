from mastodon.types import Notification
from mastodon_bot.mastodon_bot.streaming import CallbackStreamListener


class FollowingHandler(CallbackStreamListener):
    def __init__(self) -> None:
        super().__init__()

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "follow":
            print(f"{notification.account.acct} followed you")
