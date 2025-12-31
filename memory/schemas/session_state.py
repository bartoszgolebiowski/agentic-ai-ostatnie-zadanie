# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Session State Schema - current coaching session state.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SessionState(BaseModel):
    """
    Current coaching session state.
    Wszystkie pola niezbędne do zaliczenia kryteriów LC-001 do LC-014.
    """

    # Podstawowe informacje
    user_id: str = Field(..., description="Unique user identifier")
    user_name: Optional[str] = Field(default=None, description="User name (LC-002)")
    conversation_history: List[dict] = Field(
        default_factory=list, description="History of messages"
    )
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    # LC-001: Self-Introduction tracking
    coach_introduced: bool = Field(
        default=False, description="Whether coach has introduced itself (LC-001)"
    )

    # LC-002: Context gathering tracking
    context_gathered: bool = Field(
        default=False, description="Whether basic context has been collected (LC-002)"
    )

    # LC-006: Language tracking
    detected_language: str = Field(
        default="pl", description="Detected user language (LC-006)"
    )

    # Stan procesu coachingowego
    current_phase: Optional[str] = Field(
        default="INTRODUCTION", description="Current phase (LC-002)"
    )
    main_goal: Optional[str] = Field(
        default=None, description="User's main goal (LC-002)"
    )

    # Analiza jakościowa
    detected_emotions: List[str] = Field(
        default_factory=list, description="Detected emotions (LC-011)"
    )
    key_insights: List[str] = Field(
        default_factory=list, description="User insights (LC-009)"
    )
    action_plan: Optional[str] = Field(
        default=None, description="Action steps (LC-010)"
    )

    # LC-008: Thread/topic tracking
    topics: List[str] = Field(
        default_factory=list, description="Conversation topics/threads (LC-008)"
    )
    key_facts: List[str] = Field(
        default_factory=list, description="User-provided facts (LC-007, LC-008)"
    )

    # LC-010: Action steps (enhanced)
    action_steps: List[str] = Field(
        default_factory=list, description="Concrete action items (LC-010)"
    )

    # LC-014: Session summary
    session_summary: Optional[str] = Field(
        default=None, description="Session summary (LC-014)"
    )

    # Metryki techniczne (pomocne przy ewaluacji)
    paraphrases_count: int = Field(default=0, description="Counter for LC-005")
    open_questions_count: int = Field(default=0, description="Counter for LC-004")
    deepening_questions_count: int = Field(default=0, description="Counter for LC-012")
    celebrations_count: int = Field(default=0, description="Counter for LC-009")

    class Config:
        arbitrary_types_allowed = True
