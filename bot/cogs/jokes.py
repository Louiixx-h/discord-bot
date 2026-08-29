"""Agendamento da piada diária com timezone e histórico persistente."""

from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, time, timezone

import discord
from discord import app_commands
from discord.ext import commands, tasks

from bot.client import FriendsBot
from bot.config import Settings
from bot.data.jokes import JOKES
from bot.utils.channels import safe_send_to_text_channel
from bot.utils.joke_state import JokeState, JokeStateStore

LOGGER = logging.getLogger(__name__)


def choose_joke_index(total: int, last_index: int | None) -> int:
    """Escolhe um índice válido, excluindo o último quando isso for possível."""

    if total <= 0:
        raise ValueError("É necessário cadastrar pelo menos uma piada.")
    if total == 1:
        return 0
    if last_index is None or not 0 <= last_index < total:
        return random.randrange(total)

    selected = random.randrange(total - 1)
    return selected + 1 if selected >= last_index else selected


class JokesCog(commands.Cog):
    def __init__(self, bot: FriendsBot) -> None:
        self.bot = bot
        self.settings: Settings = bot.settings
        self.store = JokeStateStore(self.settings.joke_state_file)
        self._send_lock = asyncio.Lock()
        self._last_manual_joke_index: int | None = None
        self.daily_joke.change_interval(time=self.settings.daily_joke_time)

    async def cog_load(self) -> None:
        if not self.daily_joke.is_running():
            self.daily_joke.start()

    async def cog_unload(self) -> None:
        self.daily_joke.cancel()

    @app_commands.command(name="joke", description="Conta uma piada bem bobona.")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3.0, key=lambda interaction: interaction.user.id)
    async def joke(self, interaction: discord.Interaction) -> None:
        joke_index = choose_joke_index(
            len(JOKES), self._last_manual_joke_index
        )
        self._last_manual_joke_index = joke_index
        await interaction.response.send_message(
            f"{JOKES[joke_index]}",
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @tasks.loop(time=time(hour=12, tzinfo=timezone.utc))
    async def daily_joke(self) -> None:
        async with self._send_lock:
            today = datetime.now(self.settings.timezone).date()
            state = await self.store.load()
            if state.sent_date == today:
                LOGGER.info("A piada diária de hoje já foi enviada; envio ignorado.")
                return

            joke_index = choose_joke_index(len(JOKES), state.last_index)
            expected_guild_id = self.settings.guild_id
            sent = await safe_send_to_text_channel(
                self.bot,
                self.settings.general_channel_id,
                expected_guild_id=expected_guild_id,
                content=f"**Piada do dia**\n{JOKES[joke_index]}",
                allowed_mentions=discord.AllowedMentions.none(),
            )
            if sent:
                await self.store.save(
                    JokeState(last_index=joke_index, sent_date=today)
                )
                LOGGER.info("Piada diária enviada com sucesso.")

    @daily_joke.before_loop
    async def before_daily_joke(self) -> None:
        await self.bot.wait_until_ready()

    @daily_joke.error
    async def daily_joke_error(self, error: BaseException) -> None:
        LOGGER.error(
            "Erro não tratado na tarefa da piada diária (%s).",
            type(error).__name__,
            exc_info=(type(error), error, error.__traceback__),
        )


async def setup(bot: FriendsBot) -> None:
    await bot.add_cog(JokesCog(bot))
