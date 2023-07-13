import os
from mastodon import streaming, Mastodon
from mastodon.types import Notification

from dotenv import load_dotenv

load_dotenv()


api = Mastodon(
    api_base_url=os.environ.get("MASTODON_API_BASE_URL"),
    client_id=os.environ.get("MASTODON_CLIENT_KEY"),
    client_secret=os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token=os.environ.get("MASTODON_ACCESS_TOKEN"),
)


def notification_handler(notification: Notification) -> None:
    if notification.type == "mention" and notification.status.in_reply_to_id is None:
        account = notification.account
        status = notification.status

        print(notification)
        api.status_post(
            f"@{account.username} りぷらいっちゃ",
            in_reply_to_id=status.id,
        )


listener = streaming.CallbackStreamListener(
    notification_handler=notification_handler
)


api.stream_user(
    listener=listener,
    run_async=True,
    reconnect_async=True
)

if __name__ == "__main__":
    while True:
        pass
