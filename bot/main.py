"""Ponto de entrada do bot."""

from __future__ import annotations

import asyncio
import logging

import discord

from bot.client import FriendsBot
from bot.config import ConfigurationError, Settings

LOGGER = logging.getLogger(__name__)


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


async def run_bot(settings: Settings) -> None:
    async with FriendsBot(settings) as bot:
        await bot.start(settings.token, reconnect=True)


def main() -> None:
    try:
        settings = Settings.from_env()
    except ConfigurationError as exc:
        logging.basicConfig(level=logging.ERROR, format="%(levelname)s | %(message)s")
        LOGGER.critical("Configuração inválida: %s", exc)
        raise SystemExit(2) from exc

    configure_logging(settings.log_level)

    try:
        asyncio.run(run_bot(settings))
    except KeyboardInterrupt:
        LOGGER.info("Encerramento solicitado pelo usuário.")
    except discord.LoginFailure:
        LOGGER.critical("Falha de autenticação. Verifique o token configurado.")
        raise SystemExit(3) from None
    except discord.HTTPException:
        LOGGER.critical("Não foi possível estabelecer comunicação com o Discord.")
        raise SystemExit(4) from None


if __name__ == "__main__":
    main()
