# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class CoachingPhase(str, Enum):
    """Fazy procesu coachingowego."""

    INTRODUCTION = "INTRODUCTION"
    CONTEXT_GATHERING = "CONTEXT_GATHERING"
    EXPLORATION = "EXPLORATION"
    DEEPENING = "DEEPENING"
    REDIRECTING = "REDIRECTING"
    SUMMARIZING = "SUMMARIZING"
    ACTION_PLANNING = "ACTION_PLANNING"
    CLOSING = "CLOSING"


class QuestionType(str, Enum):
    """Typ pytania lub interwencji zastosowanej przez Coacha."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PARAPHRASE = "PARAPHRASE"
    DEEPENING = "DEEPENING"
    CELEBRATION = "CELEBRATION"
    SUMMARY = "SUMMARY"
    NONE = "NONE"


class CoachResponseAnalysis(BaseModel):
    """
    Strukturalna analiza odpowiedzi Coacha (Structured Output).

    Wymusza proces myślowy (Chain of Thought) przed wygenerowaniem odpowiedzi.
    """

    # KROK 1: MYŚLENIE (Chain of Thought)
    analysis_summary: str = Field(
        ...,
        description=(
            "Wewnętrzny monolog. Przeanalizuj, co użytkownik powiedział, "
            "co czuje i czy nie prosi o gotową radę."
        ),
    )

    # KROK 2: DIAGNOZA STANU
    coaching_phase: CoachingPhase = Field(
        ...,
        description="Aktualna faza procesu coachingowego na podstawie przebiegu rozmowy.",
    )

    detected_emotions: List[str] = Field(
        default_factory=list,
        description="Lista emocji wykrytych w wypowiedzi użytkownika (LC-011).",
    )

    question_type: QuestionType = Field(
        ...,
        description="Kategoria interwencji/pytania, którą zamierzasz zastosować (LC-004, LC-005, LC-012).",
    )

    # LC-002: Context extraction fields
    extracted_user_name: Optional[str] = Field(
        default=None,
        description="Imię użytkownika wykryte z jego wypowiedzi (LC-002). Null jeśli nie podane.",
    )

    extracted_goal: Optional[str] = Field(
        default=None,
        description="Cel/temat rozmowy wykryty z wypowiedzi użytkownika (LC-002). Null jeśli nie podany.",
    )

    # LC-006: Language detection
    response_language: str = Field(
        default="pl",
        description="Język odpowiedzi - MUSI być taki sam jak język użytkownika (LC-006). 'pl' lub 'en'.",
    )

    # LC-007: Fact referencing
    referenced_facts: List[str] = Field(
        default_factory=list,
        description="Lista faktów z wypowiedzi użytkownika, do których nawiązujesz (LC-007).",
    )

    # LC-008: Topic/thread tracking
    current_topic: Optional[str] = Field(
        default=None, description="Aktualny wątek/temat rozmowy (LC-008)."
    )

    # LC-009: Insight detection
    insight_detected: bool = Field(
        default=False, description="Czy użytkownik miał wgląd/odkrycie? (LC-009)"
    )

    celebration_given: bool = Field(
        default=False, description="Czy celebrujesz wgląd użytkownika? (LC-009)"
    )

    # LC-003 & LC-013: Safety self-checks
    contains_advice: bool = Field(
        default=False,
        description="SELF-CHECK: Czy odpowiedź zawiera radę? MUSI być False! (LC-003)",
    )

    contains_judgment: bool = Field(
        default=False,
        description="SELF-CHECK: Czy odpowiedź zawiera ocenę/moralizowanie? MUSI być False! (LC-013)",
    )

    # LC-010: Action step extraction
    proposed_action_step: Optional[str] = Field(
        default=None,
        description="Konkretny krok działania ustalony z użytkownikiem (LC-010).",
    )

    # KROK 3: DZIAŁANIE (Odpowiedź)
    ai_response: str = Field(
        ...,
        description=(
            "Finalna odpowiedź do użytkownika. "
            "MUSI być zgodna z Prime Directive (LC-003: brak rad) i w języku użytkownika (LC-006)."
        ),
    )
