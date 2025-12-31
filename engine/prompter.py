# -*- coding: utf-8 -*-
from __future__ import annotations

"""
System Prompter - builds dynamic system prompts using Jinja2 templates.
"""

from jinja2 import Environment, FileSystemLoader
from config import Config


class SystemPrompter:
    """
    Builds system prompts by rendering Jinja2 templates with state context.

    Supports templates from:
    - templates/ (main templates like main.j2)
    - memory/templates/ (memory layer templates like core.j2, working.j2)
    """

    def __init__(self):
        """Initialize with both template directories."""
        self.env = Environment(
            loader=FileSystemLoader(
                [
                    str(Config.TEMPLATES_DIR),  # Main templates
                    str(Config.MEMORY_TEMPLATES_DIR),  # Memory templates
                ]
            )
        )

    def build_system_prompt(
        self, core: dict, profile: dict, session: dict, history: list
    ) -> str:
        """
        Build the system prompt by rendering the main template.

        Args:
            core: Coach identity (coach_name, etc.)
            profile: User profile (user_name, main_goal)
            session: Session state (phase, turn_count, emotions, etc.)
            history: Recent conversation history

        Returns:
            Rendered system prompt string
        """
        template = self.env.get_template("main.j2")

        return template.render(
            core=core, profile=profile, session=session, history=history
        )
