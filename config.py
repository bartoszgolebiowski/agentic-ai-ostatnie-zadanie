# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Konfiguracja systemu Life Coach.

Ten plik zawiera podstawowe ustawienia. Student moze go rozbudowac
o dodatkowe parametry (np. TEMPERATURE, MAX_TOKENS, COACH_PERSONALITY).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Centralna konfiguracja systemu.

    TODO (Student): Mozesz dodac wiecej parametrow:
    - TEMPERATURE (float): Kontrola losowosci odpowiedzi (0.0-1.0)
    - MAX_TOKENS (int): Maksymalna dlugosc odpowiedzi
    - COACH_PERSONALITY (str): Opis osobowosci coacha
    - LANGUAGE (str): Preferowany jezyk ("pl" lub "en")
    """

    # Model LLM
    MODEL_NAME = "x-ai/grok-4.1-fast"  # Full model name for DataWorkshop LAB API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = "https://openrouter.ai/api/v1"  # Custom base URL

    # LLM parameters (from helper.py)
    TEMPERATURE = 0.0
    MAX_TOKENS = 10_000

    # Sprawdzenie czy klucz API istnieje
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY nie znaleziony! "
            "Upewnij sie, ze plik .env zawiera: OPENAI_API_KEY=sk-..."
        )

    # Sciezki
    BASE_DIR = Path(__file__).parent
    TEMPLATES_DIR = BASE_DIR / "templates"  # Main templates (main.j2)
    MEMORY_TEMPLATES_DIR = (
        BASE_DIR / "memory" / "templates"
    )  # Memory templates (core.j2, etc.)
    DATA_DIR = BASE_DIR / "data"  # Storage directory for file backend

    # Domyslne wartosci coacha
    COACH_NAME = "Coach Majkel Bagieta"  # TODO: Mozesz zmienic na wlasne imie (np. "Nova", "Jasiu")
    DEFAULT_USER_ID = "default_user"

    # Persistence
    PERSISTENCE_BACKEND = "file"  # Mozliwe: "in_memory", "redis", "postgres"

    # Limity konwersacji (dla context window)
    MAX_HISTORY_MESSAGES = 10  # Ile ostatnich wiadomosci przekazywac do LLM

    # Debug mode
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
