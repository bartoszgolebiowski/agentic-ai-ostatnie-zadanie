# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Safety Skills - LC-003 (No Advice) and LC-013 (Non-Judgmental)

These skill definitions handle safety checks for coach responses.
Skills are declarative - they define WHAT to check, not HOW.
"""

from pydantic import BaseModel, Field
from typing import List


class AdviceCheckOutput(BaseModel):
    """
    Output model for advice detection skill (LC-003).

    Used to validate that a response doesn't contain direct advice.
    """

    contains_advice: bool = Field(
        default=False,
        description="True if the response contains direct advice (powinieneś, musisz, etc.)",
    )
    advice_phrases_found: List[str] = Field(
        default_factory=list, description="List of advice phrases found in the response"
    )
    suggested_alternative: str = Field(
        default="", description="Suggested rephrasing as an open question"
    )


class JudgmentCheckOutput(BaseModel):
    """
    Output model for judgment detection skill (LC-013).

    Used to validate that a response doesn't contain judgmental language.
    """

    contains_judgment: bool = Field(
        default=False, description="True if the response contains judgmental language"
    )
    judgment_phrases_found: List[str] = Field(
        default_factory=list,
        description="List of judgmental phrases found in the response",
    )
    suggested_alternative: str = Field(
        default="", description="Suggested neutral rephrasing"
    )


class FactVerificationOutput(BaseModel):
    """
    Output model for fact verification skill (LC-007).

    Used to verify that referenced facts actually come from the conversation.
    """

    all_facts_verified: bool = Field(
        default=True,
        description="True if all referenced facts are from the conversation",
    )
    unverified_facts: List[str] = Field(
        default_factory=list,
        description="List of facts that were hallucinated (not in conversation)",
    )
    verified_facts: List[str] = Field(
        default_factory=list, description="List of facts that were correctly referenced"
    )


# Forbidden phrases for LC-003 (Prime Directive)
ADVICE_PHRASES_PL = [
    "powinieneś",
    "powinnaś",
    "musisz",
    "na twoim miejscu",
    "najlepiej zrób",
    "spróbuj",
    "proponuję",
    "radzę ci",
    "moim zdaniem powinieneś",
    "zrób tak",
    "nie rób tego",
]

ADVICE_PHRASES_EN = [
    "you should",
    "you must",
    "you have to",
    "i suggest",
    "i recommend",
    "try to",
    "in my opinion you should",
    "if i were you",
]

# Forbidden phrases for LC-013 (Non-Judgmental)
JUDGMENT_PHRASES_PL = [
    "to źle",
    "to głupie",
    "to nie było mądre",
    "powinieneś się wstydzić",
    "nie powinieneś tak",
    "to błąd",
    "nie rozumiem jak możesz",
]

JUDGMENT_PHRASES_EN = [
    "that's bad",
    "that's stupid",
    "that wasn't smart",
    "you should be ashamed",
    "you shouldn't",
    "that's a mistake",
    "i don't understand how you could",
]
