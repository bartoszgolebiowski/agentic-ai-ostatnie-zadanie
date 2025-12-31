# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Action Planning Skills - LC-010 (Action Planning) and LC-014 (Session Summary)

These skill definitions handle action planning and session closure.
Skills are declarative - they define WHAT to do, not HOW.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ActionStep(BaseModel):
    """
    Single action step identified during coaching.
    """

    description: str = Field(..., description="Description of the action step")
    timeframe: Optional[str] = Field(
        default=None,
        description="When this step should be completed (e.g., 'tomorrow', 'this week')",
    )
    is_small_step: bool = Field(
        default=True, description="Whether this is a small, achievable step"
    )


class ActionPlanOutput(BaseModel):
    """
    Output model for action planning skill (LC-010).

    Used when coach helps user define concrete next steps.
    """

    action_steps: List[ActionStep] = Field(
        default_factory=list,
        description="List of concrete action steps agreed with user",
    )
    primary_step: Optional[str] = Field(
        default=None, description="The single most important next step"
    )
    user_commitment_level: str = Field(
        default="unknown",
        description="User's commitment level: high, medium, low, unknown",
    )
    follow_up_question: str = Field(
        default="", description="Question to check commitment or clarify the step"
    )


class SessionSummaryOutput(BaseModel):
    """
    Output model for session summary skill (LC-014).

    Used when coach summarizes the session at the end.
    """

    key_discoveries: List[str] = Field(
        default_factory=list, description="Main insights/discoveries from the session"
    )
    emotions_explored: List[str] = Field(
        default_factory=list, description="Emotions that were explored during session"
    )
    topics_covered: List[str] = Field(
        default_factory=list, description="Main topics discussed"
    )
    action_steps: List[str] = Field(
        default_factory=list, description="Agreed action steps"
    )
    summary_text: str = Field(
        default="", description="Full text summary of the session"
    )
    closing_message: str = Field(
        default="", description="Warm closing message for the user"
    )


# Action planning question templates (LC-010)
ACTION_QUESTIONS_PL = [
    "Jaki jest jeden mały krok, który możesz zrobić jutro?",
    "Co zrobisz z tą wiedzą w tym tygodniu?",
    "Jakie konkretne działanie podejmiesz?",
    "Co będzie Twoim pierwszym krokiem?",
    "Kiedy dokładnie to zrobisz?",
    "Jak będziesz wiedział, że Ci się udało?",
]

ACTION_QUESTIONS_EN = [
    "What's one small step you can take tomorrow?",
    "What will you do with this knowledge this week?",
    "What concrete action will you take?",
    "What will be your first step?",
    "When exactly will you do this?",
    "How will you know you've succeeded?",
]

# Session summary templates (LC-014)
SUMMARY_TEMPLATES_PL = [
    "Podsumujmy, co dzisiaj odkryłeś: {discoveries}",
    "Kluczowe rzeczy z naszej rozmowy: {topics}",
    "Dzisiaj rozmawialiśmy o {topics}, a Ty odkryłeś {discoveries}",
]

SUMMARY_TEMPLATES_EN = [
    "Let's summarize what you discovered today: {discoveries}",
    "Key things from our conversation: {topics}",
    "Today we talked about {topics}, and you discovered {discoveries}",
]
