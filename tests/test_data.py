from __future__ import annotations

import unittest

from bot.data.games import GAMES
from bot.data.rules import RULES


class DataTests(unittest.TestCase):
    def test_game_catalog_has_at_least_twenty_entries(self) -> None:
        self.assertGreaterEqual(len(GAMES), 20)
        self.assertTrue(
            all(
                game.name
                and game.description
                and game.players
                and game.genre
                and game.platforms
                for game in GAMES
            )
        )

    def test_rules_have_the_expected_ten_entries(self) -> None:
        self.assertEqual(len(RULES), 10)


if __name__ == "__main__":
    unittest.main()
