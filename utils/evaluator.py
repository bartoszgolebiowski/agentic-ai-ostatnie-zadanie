# -*- coding: utf-8 -*-
"""
LLM-as-Judge Evaluator - dynamic model creation and evaluation.

Based on lesson 5.3 methodology using pydantic.create_model.
"""

from pydantic import BaseModel, Field, create_model
from typing import List, Type, Any, Dict
from .leaderboard_parser import CheckDefinition
from engine.client import get_llm_client
from config import Config


def create_evaluation_model(checks: List[CheckDefinition]) -> Type[BaseModel]:
    """
    Dynamically create Pydantic model for evaluation.

    For each check, create 2 fields:
    - {id}_reasoning: str (Chain of Thought with quoted dialog fragments)
    - {id}_passed: bool (Binary verdict)

    Args:
        checks: List of CheckDefinition to evaluate

    Returns:
        Dynamically created Pydantic model class

    Example:
        checks = [CheckDefinition(id="LC-001", ...)]
        Model = create_evaluation_model(checks)
        # Model has fields: LC_001_reasoning, LC_001_passed
    """
    fields = {}

    for check in checks:
        # Normalize ID: LC-001 -> LC_001 (pydantic field name)
        prefix = check.id.replace("-", "_")

        # Field 1: reasoning (Chain of Thought)
        fields[f"{prefix}_reasoning"] = (
            str,
            Field(
                ...,
                description=(
                    f"Analiza dla {check.id} ({check.title}). "
                    f"Kryterium: {check.description}. "
                    f"WAŻNE: Zacytuj konkretny fragment dialogu jako dowód "
                    f"lub napisz 'Brak dowodu w dialogu' jeśli kryterium nie występuje."
                ),
            ),
        )

        # Field 2: passed (Binary verdict)
        fields[f"{prefix}_passed"] = (
            bool,
            Field(
                ...,
                description=(
                    f"Werdykt binarny dla {check.id}. "
                    f"True jeśli kryterium w pełni spełnione (wszystkie elementy obecne). "
                    f"False jeśli wykryto błąd, naruszenie lub brak wymaganego elementu."
                ),
            ),
        )

    # Create model dynamically
    return create_model("DynamicEvaluationResult", **fields)


def evaluate_conversation(
    session_state: Dict[str, Any], checks: List[CheckDefinition]
) -> Dict[str, Any]:
    """
    Evaluate a full session state using LLM-as-Judge with structured output.

    Args:
        session_state: Serialized SessionState dict containing conversation_history
        checks: List of criteria to evaluate (already filtered by priority)

    Returns:
        Dict with:
        - results: List of {id, title, reasoning, passed}
        - summary: {passed_count, failed_count, total, score_pct}
        - priority: Priority group evaluated
    """
    conversation_history = (
        session_state.get("conversation_history", []) if session_state else []
    )

    if not checks:
        return {
            "error": "No checks provided for evaluation",
            "results": [],
            "summary": {},
        }

    if not conversation_history:
        return {"error": "No conversation to evaluate", "results": [], "summary": {}}

    # Create dynamic model
    EvaluationModel = create_evaluation_model(checks)

    # Format conversation for LLM
    dialog_text = "\n\n".join(
        [f"**{msg['role'].upper()}**: {msg['content']}" for msg in conversation_history]
    )

    # Build system prompt
    system_prompt = """Jesteś ekspertem od coachingu i sędzią oceniającym jakość sesji coachingowych.

Twoim zadaniem jest przeanalizować dialog i ocenić każde kryterium według podanych instrukcji.

Zasady oceny:
1. Dla każdego kryterium napisz uzasadnienie (reasoning) cytując konkretny fragment dialogu
2. Jeśli nie znajdziesz dowodu w dialogu, napisz "Brak dowodu w dialogu"
3. Wydaj werdykt (passed): True jeśli kryterium CAŁKOWICIE spełnione, False w przeciwnym razie
4. Bądź obiektywny i surowy - częściowe spełnienie = False
5. Cytuj DOKŁADNIE to co powiedziano, nie parafrazuj

Pamiętaj: To ocena JAKOŚCI coachingu, nie ilości tekstu."""

    # Build user prompt
    criteria_list = "\n".join(
        [
            f"{i+1}. {check.id} - {check.title} ({check.priority}): {check.description}"
            for i, check in enumerate(checks)
        ]
    )

    user_prompt = f"""## Dialog do oceny:

{dialog_text}

---

## Kryteria do oceny ({len(checks)} total):

{criteria_list}

---

Oceń powyższy dialog według wszystkich {len(checks)} kryteriów."""

    # Call LLM with structured output
    client = get_llm_client()

    try:
        result = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_model=EvaluationModel,
            temperature=0.0,  # Deterministic evaluation
        )
    except Exception as e:
        return {
            "error": f"LLM evaluation failed: {str(e)}",
            "results": [],
            "summary": {},
        }

    # Parse results
    results = []
    passed_count = 0

    for check in checks:
        prefix = check.id.replace("-", "_")
        reasoning = getattr(result, f"{prefix}_reasoning", "")
        passed = getattr(result, f"{prefix}_passed", False)

        if passed:
            passed_count += 1

        results.append(
            {
                "id": check.id,
                "title": check.title,
                "priority": check.priority,
                "reasoning": reasoning,
                "passed": passed,
            }
        )

    failed_count = len(checks) - passed_count
    score_pct = (passed_count / len(checks) * 100) if checks else 0

    # Determine priority group
    priority_group = checks[0].priority if checks else "UNKNOWN"
    if len(set(c.priority for c in checks)) > 1:
        priority_group = "ALL"

    summary = {
        "passed_count": passed_count,
        "failed_count": failed_count,
        "total": len(checks),
        "score_pct": round(score_pct, 1),
        "priority": priority_group,
    }

    return {"results": results, "summary": summary}


def format_evaluation_results(eval_result: Dict[str, Any]) -> str:
    """
    Format evaluation results as human-readable text for Gradio display.

    Args:
        eval_result: Output from evaluate_conversation()

    Returns:
        Formatted string with emoji indicators
    """
    if "error" in eval_result:
        return f"❌ **Error:** {eval_result['error']}"

    summary = eval_result["summary"]
    results = eval_result["results"]

    # Header
    output = f"""🎯 **Evaluation Results**

**Priority Group:** {summary['priority']}
**Score:** {summary['passed_count']}/{summary['total']} ({summary['score_pct']}%)
**Status:** {'✅ PASS' if summary['score_pct'] == 100 else '⚠️ PARTIAL' if summary['score_pct'] > 0 else '❌ FAIL'}

---

## Detailed Results:

"""

    # Individual results
    for r in results:
        icon = "✅" if r["passed"] else "❌"
        output += f"""
### {icon} {r['id']} - {r['title']} ({r['priority']})

**Verdict:** {'PASS ✅' if r['passed'] else 'FAIL ❌'}

**Reasoning:**
{r['reasoning']}

---
"""

    return output
