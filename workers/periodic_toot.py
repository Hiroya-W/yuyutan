from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
import schedule
import time

from yuyutan.jobs.periodic_toot import periodic_toot

from redis import Redis
from rq import Queue

queue = Queue(connection=Redis())


def enqueue() -> None:
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    # 今の時間から次に0分になる時間
    # ちゃんと日付もまたいでくれる
    next_ = now + timedelta(hours=1)

    # ちょうど0分に投稿
    next_ = datetime(
        next_.year, next_.month, next_.day, next_.hour, 0, tzinfo=ZoneInfo("Asia/Tokyo")
    )

    queue.enqueue_at(next_, periodic_toot)


def main() -> None:
    schedule.every(60).minutes.do(enqueue)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
