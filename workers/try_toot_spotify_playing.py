import os
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
import schedule
import random
import time

from yuyutan.jobs.toot_spotify_playing import toot_spotify_playing
from redis import Redis
from rq import Queue

from dotenv import load_dotenv

load_dotenv()

queue = Queue(connection=Redis(host=os.environ.get("REDIS_HOST", "localhost")))


def enqueue() -> None:
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    delta_hours = random.randint(1, 4)
    next_ = now + timedelta(hours=delta_hours)

    next_minutes = random.randint(0,59)

    next_ = datetime(
        next_.year, next_.month, next_.day, next_.hour, next_minutes, tzinfo=ZoneInfo("Asia/Tokyo")
    )

    queue.enqueue_at(next_, toot_spotify_playing)


def main() -> None:
    schedule.every(4).hours.do(enqueue)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
