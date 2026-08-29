"""Slash Command de recomendação de jogos."""

from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.client import FriendsBot
from bot.data.games import GAMES


class GamesCog(commands.Cog):
    def __init__(self, bot: FriendsBot) -> None:
        self.bot = bot

    @app_commands.command(
        name="jogo", description="Recomenda um jogo para curtir com os amigos."
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3.0, key=lambda interaction: interaction.user.id)
    async def game(self, interaction: discord.Interaction) -> None:
        game = random.choice(GAMES)
        embed = discord.Embed(
            title=f"🎮 Que tal jogar {game.name}?",
            description=game.description,
            color=discord.Color.blurple(),
        )
        embed.add_field(name="👥 Jogadores", value=game.players, inline=True)
        embed.add_field(name="🕹️ Tipo", value=game.genre, inline=True)
        embed.add_field(name="💻 Plataformas", value=game.platforms, inline=False)
        embed.set_footer(text="Use /jogo novamente para receber outra sugestão.")
        await interaction.response.send_message(
            embed=embed, allowed_mentions=discord.AllowedMentions.none()
        )


async def setup(bot: FriendsBot) -> None:
    await bot.add_cog(GamesCog(bot))
