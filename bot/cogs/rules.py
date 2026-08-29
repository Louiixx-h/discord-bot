"""Slash Command que exibe as regras do servidor."""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from bot.client import FriendsBot
from bot.data.rules import RULES


class RulesCog(commands.Cog):
    def __init__(self, bot: FriendsBot) -> None:
        self.bot = bot

    @app_commands.command(
        name="regras", description="Mostra as regras básicas do servidor."
    )
    @app_commands.guild_only()
    async def rules(self, interaction: discord.Interaction) -> None:
        description = "\n".join(
            f"**{number}.** {rule}" for number, rule in enumerate(RULES, start=1)
        )
        embed = discord.Embed(
            title="📜 Regras do servidor",
            description=description,
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Obrigado por ajudar a manter a comunidade agradável!")
        await interaction.response.send_message(
            embed=embed, allowed_mentions=discord.AllowedMentions.none()
        )


async def setup(bot: FriendsBot) -> None:
    await bot.add_cog(RulesCog(bot))
