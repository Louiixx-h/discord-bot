"""Persistência pequena e atômica do histórico da piada diária."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class JokeState:
    last_index: int | None = None
    sent_date: date | None = None


class JokeStateStore:
    """Lê e grava o estado sem bloquear o event loop do Discord."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = asyncio.Lock()

    async def load(self) -> JokeState:
        async with self._lock:
            return await asyncio.to_thread(self._load_sync)

    async def save(self, state: JokeState) -> None:
        async with self._lock:
            await asyncio.to_thread(self._save_sync, state)

    def _load_sync(self) -> JokeState:
        try:
            with self.path.open("r", encoding="utf-8") as state_file:
                payload = json.load(state_file)
            return _state_from_payload(payload)
        except FileNotFoundError:
            return JokeState()
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            LOGGER.warning("Estado anterior da piada é inválido ou não pôde ser lido.")
            return JokeState()

    def _save_sync(self, state: JokeState) -> None:
        payload = {
            "last_index": state.last_index,
            "sent_date": state.sent_date.isoformat() if state.sent_date else None,
        }
        temporary_name: str | None = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                json.dump(payload, temporary_file, ensure_ascii=False)
                temporary_file.write("\n")
                temporary_name = temporary_file.name
            os.replace(temporary_name, self.path)
        except OSError:
            LOGGER.exception("Não foi possível salvar o estado da piada diária.")
            if temporary_name is not None:
                try:
                    Path(temporary_name).unlink(missing_ok=True)
                except OSError:
                    pass


def _state_from_payload(payload: Any) -> JokeState:
    if not isinstance(payload, dict):
        raise ValueError("Estado deve ser um objeto JSON.")

    last_index = payload.get("last_index")
    if last_index is not None and (
        not isinstance(last_index, int)
        or isinstance(last_index, bool)
        or last_index < 0
    ):
        raise ValueError("Índice de piada inválido.")

    raw_date = payload.get("sent_date")
    sent_date = date.fromisoformat(raw_date) if isinstance(raw_date, str) else None
    return JokeState(last_index=last_index, sent_date=sent_date)
