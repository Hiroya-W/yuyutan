import os
from mastodon import streaming, Mastodon
from mastodon.types import Notification, Account

from dotenv import load_dotenv

load_dotenv()


api = Mastodon(
    api_base_url=os.environ.get("MASTODON_API_BASE_URL"),
    client_id=os.environ.get("MASTODON_CLIENT_KEY"),
    client_secret=os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token=os.environ.get("MASTODON_ACCESS_TOKEN"),
)


def reply(reply_to_id: str, from_account: Account) -> None:
    api.status_post(
        f"@{from_account.username} りぷらいっちゃ",
        in_reply_to_id=reply_to_id
    )


def notification_handler(notification: Notification) -> None:
    if notification.type == "mention" and notification.status.in_reply_to_id is None:
        account = notification.account
        status = notification.status

        reply(status.in_reply_to_id, account)


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
