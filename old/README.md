# yuyutan

## Development(in Dev Container)

redis を起動しておく。

```bash
sudo service redis-server start
```

## Install

poetry を使ってライブラリ全体をインストールしておく。

```bash
poetry install
```

## Run

Redis workerを起動しておく。

```bash
rq worker --with-scheduler
```

Pythonからjobをenqueueする。

```bash
poetry run python enqueue.py
```
