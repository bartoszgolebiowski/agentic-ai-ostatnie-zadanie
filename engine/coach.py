# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Coach Agent - główny agent coachingowy ze Structured Output.
"""

from engine.client import call_llm
from engine.prompter import SystemPrompter
from memory.schemas.session_state import SessionState
from memory.schemas.coach_types import CoachResponseAnalysis, CoachingPhase
from memory.logic.manager import MemoryManager
from config import Config


class CoachAgent:
    """
    Główny agent coachingowy.

    Używa:
    - SystemPrompter do dynamicznego budowania system promptu
    - Structured Output (CoachResponseAnalysis) do wymuszenia Chain of Thought

    Wspiera kryteria LC-001 do LC-014.
    """

    def __init__(self):
        """Inicjalizacja CoachAgent."""
        self.memory_manager = MemoryManager()
        self.prompter = SystemPrompter()

    def respond(
        self, user_message: str, state: SessionState
    ) -> tuple[str, SessionState]:
        """
        Generuje odpowiedź coacha używając Structured Output.
        """
        # 1. Dodaj wiadomość użytkownika do historii
        state = self.memory_manager.add_user_message(state, user_message)

        # 2. Pobierz kontekst ostatnich wiadomości
        recent_history = self.memory_manager.get_recent_history(
            state, limit=Config.MAX_HISTORY_MESSAGES
        )

        # 3. Zbuduj system prompt dynamicznie (wstrzykujemy stan z pamięci)
        # Przekazujemy wszystkie pola potrzebne dla kryteriów LC-001 do LC-014
        system_prompt = self.prompter.build_system_prompt(
            core={
                "coach_name": Config.COACH_NAME,
            },
            profile={
                "user_name": state.user_name,
                "main_goal": state.main_goal,
            },
            session={
                "phase": getattr(state, "current_phase", "INTRODUCTION"),
                "turn_count": len(state.conversation_history) // 2,
                "detected_emotions": state.detected_emotions,
                # LC-001: Self-introduction tracking
                "coach_introduced": state.coach_introduced,
                # LC-002: Context gathering tracking
                "context_gathered": state.context_gathered,
                # LC-006: Language tracking
                "detected_language": state.detected_language,
                # LC-007 & LC-008: Facts and topics
                "key_facts": state.key_facts,
                "topics": state.topics,
                # LC-009: Insights
                "key_insights": state.key_insights,
                # LC-010: Action steps
                "action_steps": state.action_steps,
            },
            history=recent_history,
        )

        # 4. Przygotuj strukturę wiadomości dla API
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(recent_history)

        # 5. === STRUCTURED OUTPUT ===
        # Wywołujemy LLM i oczekujemy konkretnego modelu danych
        response: CoachResponseAnalysis = call_llm(
            messages, response_model=CoachResponseAnalysis
        )

        # 6. === AKTUALIZACJA STANU ===
        # Mapujemy ustrukturyzowaną odpowiedź na trwałą pamięć sesji
        # Przekazujemy wszystkie pola z CoachResponseAnalysis
        state = self.memory_manager.update_from_output(
            state,
            {
                "response": response.ai_response,
                "ai_response": response.ai_response,
                "coaching_phase": response.coaching_phase.value,
                "detected_emotions": response.detected_emotions,
                "question_type": response.question_type.value,
                "analysis_summary": response.analysis_summary,
                # LC-002: Context extraction
                "extracted_user_name": response.extracted_user_name,
                "extracted_goal": response.extracted_goal,
                # LC-006: Language
                "response_language": response.response_language,
                # LC-007: Referenced facts
                "referenced_facts": response.referenced_facts,
                # LC-008: Topics
                "current_topic": response.current_topic,
                # LC-009: Insights and celebrations
                "insight_detected": response.insight_detected,
                "celebration_given": response.celebration_given,
                # LC-003 & LC-013: Safety checks (for debugging)
                "contains_advice": response.contains_advice,
                "contains_judgment": response.contains_judgment,
                # LC-010: Action steps
                "proposed_action_step": response.proposed_action_step,
            },
        )

        # Opcjonalny debug w konsoli
        if Config.DEBUG:
            print(f"[CoachAgent] Faza: {response.coaching_phase}")
            print(f"[CoachAgent] Typ pytania: {response.question_type}")
            print(f"[CoachAgent] Język: {response.response_language}")
            print(f"[CoachAgent] Myśli: {response.analysis_summary[:80]}...")
            if response.contains_advice:
                print(f"[CoachAgent] ⚠️ UWAGA: Odpowiedź zawiera radę!")
            if response.contains_judgment:
                print(f"[CoachAgent] ⚠️ UWAGA: Odpowiedź zawiera ocenę!")

        return response.ai_response, state
