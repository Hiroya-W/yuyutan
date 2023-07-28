FROM ubuntu:22.04

ENV PATH="/root/.rye/shims:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    rustc \
    cargo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSf https://rye-up.com/get | RYE_VERSION="0.11.0" RYE_INSTALL_OPTION="--yes" bash
