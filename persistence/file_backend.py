# -*- coding: utf-8 -*-
"""
File-based Persistence Backend

Stores each user's state as a JSON file on disk.
Intended for simple persistence across restarts (dev/demo), not for heavy prod.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
import copy

from .backend import PersistenceBackend, PersistenceError


class FileBackend(PersistenceBackend):
    """Persist user state to disk as JSON files."""

    def __init__(self, storage_dir: Path):
        """Initialize backend.

        Args:
            storage_dir: Directory where user files will be stored.
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, user_id: str) -> Path:
        return self.storage_dir / f"{user_id}.json"

    def save(self, user_id: str, state: dict) -> None:
        """Save user state to disk as JSON."""
        try:
            path = self._path_for(user_id)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=5)
        except Exception as exc:
            raise PersistenceError(
                f"Failed to save state for {user_id}: {exc}"
            ) from exc

    def load(self, user_id: str) -> Optional[dict]:
        """Load user state from disk."""
        path = self._path_for(user_id)
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return copy.deepcopy(data)
        except Exception as exc:
            raise PersistenceError(
                f"Failed to load state for {user_id}: {exc}"
            ) from exc

    def exists(self, user_id: str) -> bool:
        return self._path_for(user_id).exists()

    def delete(self, user_id: str) -> None:
        path = self._path_for(user_id)
        if not path.exists():
            raise PersistenceError(f"User {user_id} does not exist")
        try:
            path.unlink()
        except Exception as exc:
            raise PersistenceError(
                f"Failed to delete state for {user_id}: {exc}"
            ) from exc

    def list_users(self) -> list[str]:
        return [p.stem for p in self.storage_dir.glob("*.json") if p.is_file()]

    def clear_all(self) -> None:
        for p in self.storage_dir.glob("*.json"):
            if p.is_file():
                p.unlink()

    def get_storage_size(self) -> int:
        return len(self.list_users())
