# mastodon-bot-architecture

Mastodon.pyを使ったMastodonボットを作るにあたり、いい感じの設計を考えている。

## Setup

Pythonプロジェクトの依存パッケージはryeを使って管理されています。

```bash
rye sync
```

## Run

Docker Composeを使って、必要なミドルウェアを用意します。

```bash
cd docker
docker compose up -d
```

RQ Schedulerを実行します。

```bash
rye run rqscheduler --host localhost --port 6379 --interval 1 --verbose
```

最後にbotのスクリプトを実行します。

```bash
rye run python main.py
```
