# -*- coding: utf-8 -*-

from enum import Enum
from pydantic import BaseModel, Field
from typing import List


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
        )
    )
    
    # KROK 2: DIAGNOZA STANU
    coaching_phase: CoachingPhase = Field(
        ...,
        description="Aktualna faza procesu coachingowego na podstawie przebiegu rozmowy."
    )
    
    detected_emotions: List[str] = Field(
        default_factory=list,
        description="Lista emocji wykrytych w wypowiedzi użytkownika (LC-011)."
    )
    
    question_type: QuestionType = Field(
        ...,
        description="Kategoria interwencji/pytania, którą zamierzasz zastosować (LC-004, LC-005)."
    )
    
    # KROK 3: DZIAŁANIE (Odpowiedź)
    ai_response: str = Field(
        ...,
        description=(
            "Finalna odpowiedź do użytkownika. "
            "MUSI być zgodna z Prime Directive (LC-003: brak rad)."
        )
    )
