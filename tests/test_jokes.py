from __future__ import annotations

import asyncio
import tempfile
import unittest
from datetime import date
from pathlib import Path

from bot.cogs.jokes import choose_joke_index
from bot.data.jokes import JOKES
from bot.utils.joke_state import JokeState, JokeStateStore


class JokeSelectionTests(unittest.TestCase):
    def test_has_at_least_thirty_jokes(self) -> None:
        self.assertGreaterEqual(len(JOKES), 30)

    def test_never_repeats_the_previous_index(self) -> None:
        for previous in range(len(JOKES)):
            for _ in range(20):
                self.assertNotEqual(
                    choose_joke_index(len(JOKES), previous), previous
                )

    def test_rejects_empty_catalog(self) -> None:
        with self.assertRaises(ValueError):
            choose_joke_index(0, None)


class JokeStateStoreTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        async def scenario(path: Path) -> None:
            store = JokeStateStore(path)
            expected = JokeState(last_index=7, sent_date=date(2026, 8, 28))
            await store.save(expected)
            self.assertEqual(await store.load(), expected)

        with tempfile.TemporaryDirectory() as directory:
            asyncio.run(scenario(Path(directory) / "nested" / "joke.json"))

    def test_invalid_file_is_treated_as_empty_state(self) -> None:
        async def scenario(path: Path) -> None:
            store = JokeStateStore(path)
            self.assertEqual(await store.load(), JokeState())

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "joke.json"
            path.write_text("not-json", encoding="utf-8")
            asyncio.run(scenario(path))


if __name__ == "__main__":
    unittest.main()
