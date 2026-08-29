"""Resolução de canais e envio tolerante a falhas da API do Discord."""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

LOGGER = logging.getLogger(__name__)


async def safe_send_to_text_channel(
    bot: commands.Bot,
    channel_id: int,
    *,
    expected_guild_id: int | None = None,
    content: str | None = None,
    embed: discord.Embed | None = None,
    allowed_mentions: discord.AllowedMentions | None = None,
) -> bool:
    """Envia uma mensagem sem propagar falhas esperadas de canal/permissão/API."""

    channel = bot.get_channel(channel_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(channel_id)
        except discord.NotFound:
            LOGGER.warning("Canal configurado não foi encontrado.")
            return False
        except discord.Forbidden:
            LOGGER.warning("Sem permissão para consultar o canal configurado.")
            return False
        except discord.HTTPException:
            LOGGER.exception("Erro temporário ao consultar o canal configurado.")
            return False

    if not isinstance(channel, discord.TextChannel):
        LOGGER.warning("O canal configurado não é um canal de texto de servidor.")
        return False

    if expected_guild_id is not None and channel.guild.id != expected_guild_id:
        LOGGER.warning("O canal configurado pertence a outro servidor.")
        return False

    try:
        await channel.send(
            content=content,
            embed=embed,
            allowed_mentions=allowed_mentions or discord.AllowedMentions.none(),
        )
    except discord.Forbidden:
        LOGGER.warning("Sem permissão para enviar mensagem no canal configurado.")
        return False
    except discord.NotFound:
        LOGGER.warning("O canal configurado deixou de existir durante o envio.")
        return False
    except discord.HTTPException:
        LOGGER.exception("Erro temporário ao enviar mensagem no canal configurado.")
        return False
    return True
