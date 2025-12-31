from __future__ import annotations

"""
Persistence backend factory.

Selects backend based on config value.
"""

from pathlib import Path
from config import Config
from .in_memory import InMemoryBackend
from .file_backend import FileBackend


def get_backend():
    """Return the configured persistence backend instance."""
    backend = Config.PERSISTENCE_BACKEND.lower()
    if backend == "in_memory":
        return InMemoryBackend()
    if backend == "file":
        return FileBackend(Path(Config.DATA_DIR))
    raise ValueError(f"Unsupported persistence backend: {Config.PERSISTENCE_BACKEND}")
