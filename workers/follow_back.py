from mastodon import streaming, Mastodon
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from mastodon.types import Notification
import os
from yuyutan.jobs.follow_back import follow_back
from yuyutan.jobs.reply import reply
from dotenv import load_dotenv

from redis import Redis
from rq import Queue

load_dotenv()

queue = Queue(connection=Redis(host=os.environ.get("REDIS_HOST", "localhost")))

api = Mastodon(
    api_base_url=os.environ.get("MASTODON_API_BASE_URL"),
    client_id=os.environ.get("MASTODON_CLIENT_KEY"),
    client_secret=os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token=os.environ.get("MASTODON_ACCESS_TOKEN"),
)


def notification_handler(notification: Notification) -> None:
    if notification.type == "follow":
        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        next_ = now + timedelta(seconds=5)
        queue.enqueue_at(next_, follow_back, notification.account)

    if notification.type == "mention" and notification.status.in_reply_to_id is None:
        account = notification.account
        status = notification.status

        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        next_ = now + timedelta(seconds=5)
        queue.enqueue_at(next_, reply, status.id, account)


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
