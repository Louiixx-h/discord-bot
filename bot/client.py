"""Cliente Discord e sincronização controlada dos Slash Commands."""

from __future__ import annotations

import logging
import sys

import discord
from discord import app_commands
from discord.ext import commands

from bot.config import Settings

LOGGER = logging.getLogger(__name__)

EXTENSIONS = (
    "bot.cogs.welcome",
    "bot.cogs.games",
    "bot.cogs.jokes",
    "bot.cogs.rules",
    "bot.cogs.social",
)


class BotCommandTree(app_commands.CommandTree):
    """Command tree com respostas seguras para erros de Slash Commands."""

    async def on_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        root_error = getattr(error, "original", error)

        if isinstance(root_error, app_commands.CommandOnCooldown):
            message = (
                "⏳ Calma aí! Tente novamente em "
                f"{root_error.retry_after:.1f} segundos."
            )
        elif isinstance(root_error, app_commands.CheckFailure):
            message = "🚫 Este comando não está disponível neste contexto."
        else:
            command_name = interaction.command.qualified_name if interaction.command else "?"
            LOGGER.error(
                "Falha no Slash Command /%s (%s).",
                command_name,
                type(root_error).__name__,
                exc_info=(type(root_error), root_error, root_error.__traceback__),
            )
            message = "⚠️ Não consegui concluir o comando agora. Tente novamente mais tarde."

        try:
            if interaction.response.is_done():
                await interaction.followup.send(message, ephemeral=True)
            else:
                await interaction.response.send_message(message, ephemeral=True)
        except discord.HTTPException:
            LOGGER.warning("Não foi possível enviar a resposta de erro da interação.")


class FriendsBot(commands.Bot):
    """Bot com intents mínimos e ciclo de inicialização previsível."""

    def __init__(self, settings: Settings) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            help_command=None,
            allowed_mentions=discord.AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=False,
            ),
            tree_cls=BotCommandTree,
        )
        self.settings = settings

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            await self.load_extension(extension)
            LOGGER.info("Cog carregada: %s", extension)

        if self.settings.dev_guild_id is not None:
            guild = discord.Object(id=self.settings.dev_guild_id)
            self.tree.clear_commands(guild=guild)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            LOGGER.info(
                "%d Slash Command(s) sincronizado(s) no servidor de desenvolvimento.",
                len(synced),
            )
        else:
            synced = await self.tree.sync()
            LOGGER.info(
                "%d Slash Command(s) global(is) sincronizado(s).", len(synced)
            )

    async def on_ready(self) -> None:
        if self.user is not None:
            LOGGER.info(
                "Bot conectado como %s (presente em %d servidor(es)).",
                self.user,
                len(self.guilds),
            )

    async def on_disconnect(self) -> None:
        LOGGER.warning("Bot desconectado; a biblioteca tentará reconectar.")

    async def on_error(self, event_method: str, /, *args: object, **kwargs: object) -> None:
        error_type, error, traceback = sys.exc_info()
        LOGGER.error(
            "Erro não tratado no evento %s.",
            event_method,
            exc_info=(error_type, error, traceback) if error_type and error else None,
        )
