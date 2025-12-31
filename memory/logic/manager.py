# -*- coding: utf-8 -*-
from __future__ import annotations

"""
Memory Manager - zarządzanie stanem sesji coachingowej.
"""

from memory.schemas.session_state import SessionState
import copy


class MemoryManager:
    """
    Zarządza aktualizacjami pamięci na podstawie odpowiedzi coacha.
    Pattern: func(state, output) -> new_state (immutability via deep copy)
    """

    def create_empty_state(self, user_id: str) -> SessionState:
        """Inicjalizuje pusty stan dla nowego użytkownika."""
        return SessionState(
            user_id=user_id,
            user_name=None,
            conversation_history=[],
            coach_introduced=False,
            context_gathered=False,
            detected_language="pl",
        )

    def update_from_output(
        self, state: SessionState, coach_output: dict
    ) -> SessionState:
        """
        Główna logika aktualizacji stanu na podstawie analizy LLM.
        Tutaj mapujemy Structured Output na trwałą pamięć.
        """
        # 1. Tworzymy bezpieczną kopię stanu (immutability)
        updated_state = state.model_copy(deep=True)

        # LC-001: Mark coach as introduced after first response
        updated_state = self._update_introduction_status(updated_state, coach_output)

        # LC-002: Extract user context (name, goal)
        updated_state = self._extract_user_context(updated_state, coach_output)

        # LC-006: Update detected language
        updated_state = self._update_language(updated_state, coach_output)

        # LC-007 & LC-008: Track facts and topics
        updated_state = self._update_facts_and_topics(updated_state, coach_output)

        # LC-009: Track insights and celebrations
        updated_state = self._update_insights(updated_state, coach_output)

        # LC-010: Track action steps
        updated_state = self._update_action_steps(updated_state, coach_output)

        # 3. Zarządzanie fazą procesu
        if "coaching_phase" in coach_output:
            updated_state.current_phase = coach_output["coaching_phase"]

        # 4. Akumulacja wykrytych emocji (LC-011)
        if "detected_emotions" in coach_output:
            for emotion in coach_output["detected_emotions"]:
                if emotion and emotion not in updated_state.detected_emotions:
                    updated_state.detected_emotions.append(emotion)

        # 5. Aktualizacja liczników jakościowych (LC-004, LC-005, LC-012)
        updated_state = self._update_question_counters(updated_state, coach_output)

        # 6. Zapis odpowiedzi do historii dialogu
        final_text = coach_output.get("ai_response") or coach_output.get("response")
        if final_text:
            updated_state.conversation_history.append(
                {"role": "assistant", "content": final_text}
            )

        return updated_state

    def _update_introduction_status(
        self, state: SessionState, coach_output: dict
    ) -> SessionState:
        """LC-001: Mark coach as introduced after first response."""
        if not state.coach_introduced:
            # First response means coach has introduced itself
            state.coach_introduced = True
        return state

    def _extract_user_context(
        self, state: SessionState, coach_output: dict
    ) -> SessionState:
        """LC-002: Extract user name and goal from LLM output."""
        # Extract user name if detected
        extracted_name = coach_output.get("extracted_user_name")
        if extracted_name and not state.user_name:
            state.user_name = extracted_name

        # Also check legacy field
        if "user_name" in coach_output and coach_output["user_name"]:
            state.user_name = coach_output["user_name"]

        # Extract goal if detected
        extracted_goal = coach_output.get("extracted_goal")
        if extracted_goal and not state.main_goal:
            state.main_goal = extracted_goal

        # Also check legacy field
        if "main_goal" in coach_output and coach_output["main_goal"]:
            state.main_goal = coach_output["main_goal"]

        # Mark context as gathered when we have both name and goal
        if state.user_name and state.main_goal:
            state.context_gathered = True

        return state

    def _update_language(self, state: SessionState, coach_output: dict) -> SessionState:
        """LC-006: Update detected language."""
        response_lang = coach_output.get("response_language")
        if response_lang:
            state.detected_language = response_lang
        return state

    def _update_facts_and_topics(
        self, state: SessionState, coach_output: dict
    ) -> SessionState:
        """LC-007 & LC-008: Track referenced facts and conversation topics."""
        # Track facts
        referenced_facts = coach_output.get("referenced_facts", [])
        for fact in referenced_facts:
            if fact and fact not in state.key_facts:
                state.key_facts.append(fact)

        # Track current topic
        current_topic = coach_output.get("current_topic")
        if current_topic and current_topic not in state.topics:
            state.topics.append(current_topic)

        return state

    def _update_insights(self, state: SessionState, coach_output: dict) -> SessionState:
        """LC-009: Track user insights and celebrations."""
        if coach_output.get("insight_detected"):
            # Extract insight from analysis if available
            analysis = coach_output.get("analysis_summary", "")
            if analysis and len(analysis) > 10:
                # Store a summary of the insight
                insight_summary = analysis[:200] if len(analysis) > 200 else analysis
                if insight_summary not in state.key_insights:
                    state.key_insights.append(insight_summary)

        if coach_output.get("celebration_given"):
            state.celebrations_count += 1

        return state

    def _update_action_steps(
        self, state: SessionState, coach_output: dict
    ) -> SessionState:
        """LC-010: Track proposed action steps."""
        proposed_step = coach_output.get("proposed_action_step")
        if proposed_step and proposed_step not in state.action_steps:
            state.action_steps.append(proposed_step)
            # Also update legacy field
            state.action_plan = "; ".join(state.action_steps)
        return state

    def _update_question_counters(
        self, state: SessionState, coach_output: dict
    ) -> SessionState:
        """LC-004, LC-005, LC-012: Update question type counters."""
        q_type = coach_output.get("question_type")
        if q_type == "OPEN":
            state.open_questions_count += 1
        elif q_type == "PARAPHRASE":
            state.paraphrases_count += 1
        elif q_type == "DEEPENING":
            state.deepening_questions_count += 1
        elif q_type == "CELEBRATION":
            state.celebrations_count += 1
        return state

    def add_user_message(self, state: SessionState, message: str) -> SessionState:
        """Dodaje wiadomość użytkownika do historii."""
        updated_state = state.model_copy(deep=True)
        updated_state.conversation_history.append({"role": "user", "content": message})
        return updated_state

    def get_recent_history(self, state: SessionState, limit: int = 10) -> list[dict]:
        """Pobiera kontekst ostatnich N wiadomości."""
        return state.conversation_history[-limit:]

    def set_session_summary(self, state: SessionState, summary: str) -> SessionState:
        """LC-014: Set session summary."""
        updated_state = state.model_copy(deep=True)
        updated_state.session_summary = summary
        return updated_state
