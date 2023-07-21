import time
from mastodon import streaming, Mastodon
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from mastodon.types import Notification
import os
from dotenv import load_dotenv

from redis import Redis
from rq import Queue
from yuyutan.jobs.reply import reply, reply_spotify_now_playing
from yuyutan.spotify.get_playing import get_playing


MAX_REPLY_LENGTH = 5


load_dotenv()

queue = Queue(connection=Redis(host=os.environ.get("REDIS_HOST", "localhost")))

api = Mastodon(
    api_base_url=os.environ.get("MASTODON_API_BASE_URL"),
    client_id=os.environ.get("MASTODON_CLIENT_KEY"),
    client_secret=os.environ.get("MASTODON_CLIENT_SECRET"),
    access_token=os.environ.get("MASTODON_ACCESS_TOKEN"),
)


def notification_handler(notification: Notification) -> None:
    if notification.type == "mention":
        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        next_ = now + timedelta(seconds=5)

        account = notification.account
        status = notification.status
        content = notification.status.content

        if "今何聞いてる？" in content:
            url = get_playing()
            queue.enqueue_at(next_, reply_spotify_now_playing, status.id, account, url=url)
        else:
            context = api.status_context(
                status.id
            )

            if len(context.ancestors) < MAX_REPLY_LENGTH:
                queue.enqueue_at(next_, reply, status.id, account, content=notification.status.content)


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
        time.sleep(1)
