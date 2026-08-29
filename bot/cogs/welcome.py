"""Mensagens de entrada e saída de membros."""

from __future__ import annotations

import discord
from discord.ext import commands

from bot.client import FriendsBot
from bot.config import Settings
from bot.utils.channels import safe_send_to_text_channel


class WelcomeCog(commands.Cog):
    def __init__(self, bot: FriendsBot) -> None:
        self.bot = bot
        self.settings: Settings = bot.settings

    def _accepts_guild(self, guild_id: int) -> bool:
        return self.settings.guild_id is None or self.settings.guild_id == guild_id

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if not self._accepts_guild(member.guild.id):
            return

        await safe_send_to_text_channel(
            self.bot,
            self.settings.welcome_channel_id,
            expected_guild_id=member.guild.id,
            content=(
                f"🎉 Bem-vindo(a), {member.mention}! "
                "Esperamos que você se divirta por aqui!"
            ),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False, users=[member], replied_user=False
            ),
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        if not self._accepts_guild(member.guild.id):
            return

        await safe_send_to_text_channel(
            self.bot,
            self.settings.welcome_channel_id,
            expected_guild_id=member.guild.id,
            content=f"👋 {member.mention} saiu do servidor. Até a próxima!",
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False, users=[member], replied_user=False
            ),
        )


async def setup(bot: FriendsBot) -> None:
    await bot.add_cog(WelcomeCog(bot))
