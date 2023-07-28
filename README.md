# mastodon-bot-architecture

Mastodon.pyを使ったMastodonボットを作るにあたり、いい感じの設計を考えている。

## Setup

Pythonプロジェクトの依存パッケージはryeを使って管理されています。

```bash
rye sync
```

## Development

Docker Composeを使って、必要なミドルウェアを用意します。

```bash
cd docker
docker compose up -d -f docker-compose.dev.yml
```

RQ Workerを実行します。

```bash
rye run rq worker --url redis://localhost:6379 --with-scheduler
```

RQ Schedulerを実行します。

```bash
rye run rqscheduler --host localhost --port 6379 --interval 1 --verbose
```

最後にbotのスクリプトを実行します。

```bash
rye run python main.py
```

## Production

Docker Composeを使ってコンテナを立ち上げます。開発環境とは違い、ここでは`docker-compose.yml`を元にします。

```bash
cd docker
docker compose up -d
```
