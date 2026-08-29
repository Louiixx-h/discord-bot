from __future__ import annotations

import unittest

from bot.config import ConfigurationError, Settings


class SettingsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_environment = {
            "DISCORD_TOKEN": "token-de-teste",
            "WELCOME_CHANNEL_ID": "123456789012345678",
            "GENERAL_CHANNEL_ID": "223456789012345678",
            "GUILD_ID": "323456789012345678",
            "DEV_GUILD_ID": "",
            "TIMEZONE": "America/Sao_Paulo",
            "DAILY_JOKE_TIME": "12:05",
        }

    def test_loads_valid_settings(self) -> None:
        settings = Settings.from_env(self.valid_environment)

        self.assertEqual(settings.welcome_channel_id, 123456789012345678)
        self.assertEqual(settings.daily_joke_time.hour, 12)
        self.assertEqual(settings.daily_joke_time.minute, 5)
        self.assertEqual(settings.timezone_name, "America/Sao_Paulo")
        self.assertNotIn("token-de-teste", repr(settings))

    def test_requires_token(self) -> None:
        environment = {**self.valid_environment, "DISCORD_TOKEN": ""}

        with self.assertRaisesRegex(ConfigurationError, "DISCORD_TOKEN"):
            Settings.from_env(environment)

    def test_rejects_invalid_snowflake_without_echoing_value(self) -> None:
        invalid_value = "não-e-um-id"
        environment = {
            **self.valid_environment,
            "WELCOME_CHANNEL_ID": invalid_value,
        }

        with self.assertRaises(ConfigurationError) as context:
            Settings.from_env(environment)

        self.assertNotIn(invalid_value, str(context.exception))

    def test_rejects_invalid_time(self) -> None:
        environment = {**self.valid_environment, "DAILY_JOKE_TIME": "25:90"}

        with self.assertRaisesRegex(ConfigurationError, "horário válido"):
            Settings.from_env(environment)

    def test_rejects_invalid_timezone(self) -> None:
        environment = {**self.valid_environment, "TIMEZONE": "Planeta/Desconhecido"}

        with self.assertRaisesRegex(ConfigurationError, "base IANA"):
            Settings.from_env(environment)


if __name__ == "__main__":
    unittest.main()
