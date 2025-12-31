# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Context Skills - LC-001 (Introduction), LC-002 (Context Gathering), LC-005 (Paraphrasing)

These skill definitions handle context gathering and mirroring.
Skills are declarative - they define WHAT to do, not HOW.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class IntroductionOutput(BaseModel):
    """
    Output model for introduction skill (LC-001).

    Used for the first message when coach introduces itself.
    """

    coach_name: str = Field(..., description="Name of the coach")
    role_description: str = Field(
        ..., description="Description of coach's role (e.g., 'coach strategiczny')"
    )
    greeting: str = Field(
        ..., description="Full greeting message including name and role"
    )
    asks_for_name: bool = Field(
        default=True, description="Whether the greeting asks for user's name"
    )


class ContextGatheringOutput(BaseModel):
    """
    Output model for context gathering skill (LC-002).

    Used to extract basic context from user's messages.
    """

    extracted_name: Optional[str] = Field(
        default=None, description="User's name if mentioned"
    )
    extracted_goal: Optional[str] = Field(
        default=None, description="User's goal/topic if mentioned"
    )
    context_complete: bool = Field(
        default=False, description="True if we have both name and goal"
    )
    missing_context: List[str] = Field(
        default_factory=list,
        description="List of missing context elements: 'name', 'goal'",
    )
    follow_up_question: str = Field(
        default="", description="Question to gather missing context"
    )


class ParaphraseOutput(BaseModel):
    """
    Output model for paraphrasing skill (LC-005).

    Used when coach mirrors user's statement.
    """

    original_statement: str = Field(
        ..., description="User's original statement being paraphrased"
    )
    paraphrase: str = Field(..., description="Coach's paraphrase of the statement")
    paraphrase_type: str = Field(
        default="reflection",
        description="Type: 'reflection', 'summary', 'clarification'",
    )
    follow_up_question: str = Field(
        default="", description="Open question following the paraphrase"
    )


# Introduction templates (LC-001)
INTRODUCTION_TEMPLATES_PL = [
    "Cześć! Jestem {name}, Twój osobisty coach strategiczny. Będę Ci towarzyszyć w poszukiwaniu rozwiązań. Jak masz na imię?",
    "Dzień dobry! Nazywam się {name}. Jestem Twoim coachem i partnerem w rozwoju. Jak mogę się do Ciebie zwracać?",
    "Witaj! Jestem {name}, coach strategiczny. Moją rolą jest pomagać Ci odkrywać własne odpowiedzi. Jak masz na imię i z czym dzisiaj przychodzisz?",
]

INTRODUCTION_TEMPLATES_EN = [
    "Hi! I'm {name}, your personal strategic coach. I'll accompany you in finding solutions. What's your name?",
    "Hello! My name is {name}. I'm your coach and development partner. How may I address you?",
    "Welcome! I'm {name}, a strategic coach. My role is to help you discover your own answers. What's your name and what brings you here today?",
]

# Paraphrase starters (LC-005)
PARAPHRASE_STARTERS_PL = [
    "Słyszę, że...",
    "Rozumiem, że...",
    "Czyli jeśli dobrze rozumiem...",
    "Z tego co mówisz, wynika że...",
    "Wygląda na to, że...",
    "Jeśli dobrze Cię rozumiem...",
]

PARAPHRASE_STARTERS_EN = [
    "I hear that...",
    "I understand that...",
    "So if I understand correctly...",
    "From what you're saying...",
    "It seems that...",
    "If I understand you correctly...",
]

# Context gathering questions (LC-002)
CONTEXT_QUESTIONS_PL = {
    "name": [
        "Jak masz na imię?",
        "Jak mogę się do Ciebie zwracać?",
    ],
    "goal": [
        "Z czym dzisiaj przychodzisz?",
        "O czym chciałbyś dzisiaj porozmawiać?",
        "Co Cię tu sprowadza?",
    ],
}

CONTEXT_QUESTIONS_EN = {
    "name": [
        "What's your name?",
        "How may I address you?",
    ],
    "goal": [
        "What brings you here today?",
        "What would you like to talk about?",
        "What's on your mind?",
    ],
}
