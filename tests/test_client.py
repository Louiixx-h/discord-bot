from __future__ import annotations

import unittest
from unittest.mock import AsyncMock

from bot.client import EXTENSIONS, FriendsBot
from bot.config import Settings


class ClientSmokeTests(unittest.IsolatedAsyncioTestCase):
    async def test_loads_all_cogs_and_registers_slash_commands(self) -> None:
        settings = Settings.from_env(
            {
                "DISCORD_TOKEN": "token-de-teste",
                "WELCOME_CHANNEL_ID": "123456789012345678",
                "GENERAL_CHANNEL_ID": "223456789012345678",
                "TIMEZONE": "America/Sao_Paulo",
                "DAILY_JOKE_TIME": "12:00",
            }
        )
        bot = FriendsBot(settings)
        bot.tree.sync = AsyncMock(return_value=[])

        try:
            await bot.setup_hook()

            self.assertTrue(bot.intents.guilds)
            self.assertTrue(bot.intents.members)
            self.assertFalse(bot.intents.message_content)
            self.assertFalse(bot.intents.presences)
            self.assertEqual(
                {command.name for command in bot.tree.get_commands()},
                {"jogo", "regras", "joke", "aura", "zika"},
            )
            self.assertEqual(
                set(bot.cogs),
                {"WelcomeCog", "GamesCog", "JokesCog", "RulesCog", "SocialCog"},
            )
            bot.tree.sync.assert_awaited_once_with()
        finally:
            for extension in reversed(EXTENSIONS):
                if extension in bot.extensions:
                    await bot.unload_extension(extension)
            await bot.close()

    async def test_development_sync_targets_only_configured_guild(self) -> None:
        settings = Settings.from_env(
            {
                "DISCORD_TOKEN": "token-de-teste",
                "WELCOME_CHANNEL_ID": "123456789012345678",
                "GENERAL_CHANNEL_ID": "223456789012345678",
                "DEV_GUILD_ID": "323456789012345678",
            }
        )
        bot = FriendsBot(settings)
        bot.tree.sync = AsyncMock(return_value=[])

        try:
            await bot.setup_hook()

            sync_call = bot.tree.sync.await_args
            synced_guild = sync_call.kwargs["guild"]
            self.assertEqual(synced_guild.id, settings.dev_guild_id)
            self.assertEqual(
                {command.name for command in bot.tree.get_commands(guild=synced_guild)},
                {"jogo", "regras", "joke", "aura", "zika"},
            )
        finally:
            for extension in reversed(EXTENSIONS):
                if extension in bot.extensions:
                    await bot.unload_extension(extension)
            await bot.close()


if __name__ == "__main__":
    unittest.main()
