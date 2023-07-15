from mastodon.types import Notification
from mastodon_bot.mastodon_bot.streaming import CallbackStreamListener


class ReplyHandler(CallbackStreamListener):
    def __init__(self) -> None:
        super().__init__()

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "mention":
            print(f"{notification.account.acct} mentioned you")
