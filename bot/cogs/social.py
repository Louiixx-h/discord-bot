"""Comandos sociais leves para interações entre membros."""

from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.client import FriendsBot

AURA_MIN = -10_000
AURA_MAX = 1_100


def roll_aura() -> int:
    """Sorteia uma variação de aura dentro dos limites do comando."""

    return random.randint(AURA_MIN, AURA_MAX)


def format_aura(value: int) -> str:
    """Formata a aura com sinal explícito, inclusive para zero."""

    return f"{value:+d} aura"


def mentions_only(member: discord.Member) -> discord.AllowedMentions:
    """Permite mencionar exclusivamente o membro escolhido no Slash Command."""

    return discord.AllowedMentions(
        everyone=False,
        roles=False,
        users=[member],
        replied_user=False,
    )


class SocialCog(commands.Cog):
    def __init__(self, bot: FriendsBot) -> None:
        self.bot = bot

    @app_commands.command(
        name="aura", description="Sorteia a variação de aura de um membro."
    )
    @app_commands.describe(member="Membro cuja aura será medida")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3.0, key=lambda interaction: interaction.user.id)
    async def aura(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        aura = format_aura(roll_aura())
        await interaction.response.send_message(
            f"✨ {member.mention} recebeu **{aura}**!",
            allowed_mentions=mentions_only(member),
        )

    @app_commands.command(name="zika", description="Zika um membro do servidor.")
    @app_commands.describe(member="Membro que será zikado")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3.0, key=lambda interaction: interaction.user.id)
    async def zika(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        await interaction.response.send_message(
            f"🧿 {member.mention} foi zikado!",
            allowed_mentions=mentions_only(member),
        )


async def setup(bot: FriendsBot) -> None:
    await bot.add_cog(SocialCog(bot))
