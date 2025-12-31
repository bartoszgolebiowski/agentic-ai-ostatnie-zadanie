# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Exploration Skills - LC-004 (Open Questions), LC-011 (Emotion Recognition), LC-012 (Deepening Questions)

These skill definitions handle exploration and deepening conversations.
Skills are declarative - they define WHAT to do, not HOW.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class OpenQuestionOutput(BaseModel):
    """
    Output model for open question skill (LC-004).

    Used when coach asks exploratory open questions.
    """

    question: str = Field(
        ..., description="The open question (must start with Co, Jak, Dlaczego, etc.)"
    )
    question_starter: str = Field(
        ...,
        description="The question starter used: Co, Jak, Dlaczego, Kiedy, W jaki sposób",
    )
    purpose: str = Field(
        default="exploration",
        description="Purpose: exploration, clarification, emotion, values",
    )


class EmotionRecognitionOutput(BaseModel):
    """
    Output model for emotion recognition skill (LC-011).

    Used when coach identifies and names emotions.
    """

    detected_emotions: List[str] = Field(
        default_factory=list, description="List of emotions detected in user's message"
    )
    primary_emotion: Optional[str] = Field(
        default=None, description="The dominant emotion"
    )
    emotion_intensity: str = Field(
        default="medium", description="Intensity: low, medium, high"
    )
    empathetic_response: str = Field(
        default="", description="Empathetic acknowledgment of the emotion"
    )


class DeepeningQuestionOutput(BaseModel):
    """
    Output model for deepening question skill (LC-012).

    Used when coach explores meaning and values.
    """

    question: str = Field(
        ..., description="The deepening question about meaning/values"
    )
    explores: str = Field(
        default="meaning",
        description="What it explores: meaning, values, beliefs, motivations",
    )
    context_reference: Optional[str] = Field(
        default=None, description="What user statement this deepens"
    )


class InsightCelebrationOutput(BaseModel):
    """
    Output model for insight celebration skill (LC-009).

    Used when user has a breakthrough or discovery.
    """

    insight_summary: str = Field(..., description="Summary of user's insight")
    celebration_message: str = Field(..., description="Message celebrating the insight")
    follow_up_question: str = Field(
        default="", description="Question to deepen the insight"
    )


# Open question starters (LC-004)
OPEN_QUESTION_STARTERS_PL = [
    "Co",  # Co czujesz? Co to dla Ciebie znaczy?
    "Jak",  # Jak to wpływa na Ciebie? Jak się z tym czujesz?
    "Dlaczego",  # Dlaczego to jest ważne? Dlaczego tak myślisz?
    "Kiedy",  # Kiedy to się zaczęło? Kiedy czujesz się najlepiej?
    "W jaki sposób",  # W jaki sposób chciałbyś to zmienić?
    "Gdzie",  # Gdzie widzisz siebie za rok?
    "Kto",  # Kto mógłby Ci pomóc?
]

OPEN_QUESTION_STARTERS_EN = [
    "What",  # What do you feel? What does this mean to you?
    "How",  # How does this affect you? How do you feel about it?
    "Why",  # Why is this important? Why do you think so?
    "When",  # When did this start? When do you feel best?
    "In what way",  # In what way would you like to change this?
    "Where",  # Where do you see yourself in a year?
    "Who",  # Who could help you?
]

# Deepening questions (LC-012)
DEEPENING_QUESTIONS_PL = [
    "Co to dla Ciebie oznacza?",
    "Dlaczego to jest dla Ciebie tak ważne?",
    "Co za tym stoi?",
    "Jakie wartości są tu dla Ciebie kluczowe?",
    "Co to mówi o tym, kim jesteś?",
    "Skąd to się wzięło?",
    "Co by się zmieniło, gdybyś to osiągnął?",
]

DEEPENING_QUESTIONS_EN = [
    "What does this mean to you?",
    "Why is this so important to you?",
    "What's behind this?",
    "What values are key here for you?",
    "What does this say about who you are?",
    "Where does this come from?",
    "What would change if you achieved this?",
]

# Emotion naming phrases (LC-011)
EMOTION_NAMING_PL = [
    "Słyszę w Twoich słowach {emotion}...",
    "Widzę, że to wywołuje w Tobie {emotion}...",
    "Wygląda na to, że czujesz {emotion}...",
    "Słyszę {emotion} w tym, co mówisz...",
    "Rozpoznaję {emotion} w Twojej wypowiedzi...",
]

EMOTION_NAMING_EN = [
    "I hear {emotion} in your words...",
    "I see this evokes {emotion} in you...",
    "It seems you're feeling {emotion}...",
    "I hear {emotion} in what you're saying...",
    "I recognize {emotion} in your words...",
]

# Common emotions to detect
EMOTIONS_PL = [
    "frustracja",
    "lęk",
    "smutek",
    "złość",
    "radość",
    "nadzieja",
    "niepewność",
    "wdzięczność",
    "ulga",
    "entuzjazm",
    "zmęczenie",
    "rozczarowanie",
    "ekscytacja",
    "spokój",
    "niepokój",
    "duma",
]

EMOTIONS_EN = [
    "frustration",
    "fear",
    "sadness",
    "anger",
    "joy",
    "hope",
    "uncertainty",
    "gratitude",
    "relief",
    "enthusiasm",
    "fatigue",
    "disappointment",
    "excitement",
    "calm",
    "anxiety",
    "pride",
]

# Celebration phrases (LC-009)
CELEBRATION_PHRASES_PL = [
    "To potężne spostrzeżenie!",
    "Świetnie, że to zauważyłeś - to duży krok naprzód!",
    "To ważna świadomość!",
    "To naprawdę głęboki wgląd!",
    "Widzę, że właśnie coś odkryłeś - to jest naprawdę wartościowe!",
    "To przełomowa myśl!",
]

CELEBRATION_PHRASES_EN = [
    "That's a powerful insight!",
    "Great that you noticed this - it's a big step forward!",
    "That's an important awareness!",
    "That's a really deep insight!",
    "I see you just discovered something - that's really valuable!",
    "That's a breakthrough thought!",
]
