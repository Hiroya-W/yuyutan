#!/bin/sh

set -e

rye sync -f
# Redis Queueに登録されたジョブを実行するWorker
# Workerもファイルにログ出力するようにする(自分でexception handlerをセットしたWorkerを書く)
rye run rq worker --url redis://redis:6379 --with-scheduler &
# Redis Queueに登録していくScheduler
rye run rqscheduler --host redis --port 6379 --interval 1 &
rye run python main.py &
