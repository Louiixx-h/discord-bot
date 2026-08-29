from __future__ import annotations

import unittest
from unittest.mock import patch

from bot.cogs.social import AURA_MAX, AURA_MIN, format_aura, roll_aura


class AuraTests(unittest.TestCase):
    def test_formats_positive_negative_and_zero_values(self) -> None:
        self.assertEqual(format_aura(1_100), "+1100 aura")
        self.assertEqual(format_aura(-10_000), "-10000 aura")
        self.assertEqual(format_aura(0), "+0 aura")

    def test_roll_includes_configured_limits(self) -> None:
        with patch("bot.cogs.social.random.randint", return_value=AURA_MIN) as randint:
            self.assertEqual(roll_aura(), AURA_MIN)
            randint.assert_called_once_with(AURA_MIN, AURA_MAX)


if __name__ == "__main__":
    unittest.main()
