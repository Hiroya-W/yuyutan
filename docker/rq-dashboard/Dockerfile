FROM python:3.11.4-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install git+https://github.com/Parallels/rq-dashboard.git@dad4aae899f9c06e118a4f621d8d6f9d034abf7a
