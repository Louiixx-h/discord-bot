"""Carregamento e validação centralizada das configurações do bot."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import time
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv

MAX_SNOWFLAKE = (1 << 64) - 1
VALID_LOG_LEVELS = frozenset({"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"})


class ConfigurationError(RuntimeError):
    """Indica uma configuração ausente ou inválida sem expor segredos."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Configurações validadas usadas por todos os componentes do bot."""

    token: str = field(repr=False)
    welcome_channel_id: int
    general_channel_id: int
    guild_id: int | None
    dev_guild_id: int | None
    timezone_name: str
    timezone: ZoneInfo = field(repr=False)
    daily_joke_time: time
    joke_state_file: Path
    log_level: str

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        """Cria as configurações a partir do ambiente e, por padrão, do `.env`."""

        if environ is None:
            load_dotenv()
            environ = os.environ

        token = environ.get("DISCORD_TOKEN", "").strip()
        if not token:
            raise ConfigurationError("DISCORD_TOKEN é obrigatório.")

        welcome_channel_id = _parse_snowflake(
            environ, "WELCOME_CHANNEL_ID", required=True
        )
        general_channel_id = _parse_snowflake(
            environ, "GENERAL_CHANNEL_ID", required=True
        )
        guild_id = _parse_snowflake(environ, "GUILD_ID", required=False)
        dev_guild_id = _parse_snowflake(environ, "DEV_GUILD_ID", required=False)

        timezone_name = environ.get("TIMEZONE", "America/Sao_Paulo").strip()
        if not timezone_name:
            raise ConfigurationError("TIMEZONE não pode ficar vazio.")
        try:
            timezone = ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError as exc:
            raise ConfigurationError(
                "TIMEZONE deve ser um nome válido da base IANA, como America/Sao_Paulo."
            ) from exc

        daily_joke_time = _parse_time(
            environ.get("DAILY_JOKE_TIME", "12:00"), timezone
        )

        state_value = environ.get(
            "JOKE_STATE_FILE", ".state/joke_state.json"
        ).strip()
        if not state_value:
            raise ConfigurationError("JOKE_STATE_FILE não pode ficar vazio.")

        log_level = environ.get("LOG_LEVEL", "INFO").strip().upper()
        if log_level not in VALID_LOG_LEVELS:
            raise ConfigurationError(
                "LOG_LEVEL deve ser CRITICAL, ERROR, WARNING, INFO ou DEBUG."
            )

        return cls(
            token=token,
            welcome_channel_id=welcome_channel_id,
            general_channel_id=general_channel_id,
            guild_id=guild_id,
            dev_guild_id=dev_guild_id,
            timezone_name=timezone_name,
            timezone=timezone,
            daily_joke_time=daily_joke_time,
            joke_state_file=Path(state_value),
            log_level=log_level,
        )


def _parse_snowflake(
    environ: Mapping[str, str], name: str, *, required: bool
) -> int | None:
    value = environ.get(name, "").strip()
    if not value:
        if required:
            raise ConfigurationError(f"{name} é obrigatório.")
        return None

    if not value.isdecimal():
        raise ConfigurationError(f"{name} deve conter somente dígitos.")

    snowflake = int(value)
    if snowflake <= 0 or snowflake > MAX_SNOWFLAKE:
        raise ConfigurationError(f"{name} está fora do intervalo válido.")
    return snowflake


def _parse_time(value: str, timezone: ZoneInfo) -> time:
    parts = value.strip().split(":")
    if len(parts) != 2 or any(not part.isdecimal() for part in parts):
        raise ConfigurationError("DAILY_JOKE_TIME deve usar o formato HH:MM.")

    hour, minute = (int(part) for part in parts)
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ConfigurationError("DAILY_JOKE_TIME deve ser um horário válido.")
    return time(hour=hour, minute=minute, tzinfo=timezone)
