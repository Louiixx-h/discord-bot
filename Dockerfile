FROM python:3.12.14-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --system --gid 10001 discordbot \
    && useradd --system --uid 10001 --gid discordbot \
        --home-dir /app --shell /usr/sbin/nologin discordbot

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --requirement requirements.txt

COPY --chown=discordbot:discordbot bot ./bot

RUN mkdir --parents /app/.state \
    && chown --recursive discordbot:discordbot /app/.state

USER discordbot

STOPSIGNAL SIGINT

CMD ["python", "-m", "bot"]
