"""Settings module."""

import sys
from pathlib import Path
from typing import Optional

from openbb import obb
from openbb_core.app.model.abstract.singleton import SingletonMeta
from openbb_core.app.model.user_settings import UserSettings as User
from prompt_toolkit import PromptSession

from openbb_cli.argparse_translator.obbject_registry import Registry
from openbb_cli.config.completer import CustomFileHistory
from openbb_cli.config.console import Console
from openbb_cli.config.constants import HIST_FILE_PROMPT
from openbb_cli.config.style import Style
from openbb_cli.models.settings import Settings


class Session(metaclass=SingletonMeta):
    """Session class."""

    def __init__(self):
        """Initialize session."""
        self._obb = obb
        self._settings = Settings()
        self._style = Style(
            style=self._settings.RICH_STYLE,
            directory=Path(self._obb.user.preferences.user_styles_directory),  # type: ignore[union-attr]
        )
        self._console = Console(
            settings=self._settings, style=self._style.console_style
        )
        self._prompt_session = self._get_prompt_session()
        self._obbject_registry = Registry()

    @property
    def user(self) -> User:
        """Get platform user."""
        return self._obb.user  # type: ignore[union-attr]

    @property
    def settings(self) -> Settings:
        """Get CLI settings."""
        return self._settings

    @property
    def style(self) -> Style:
        """Get CLI style."""
        return self._style

    @property
    def console(self) -> Console:
        """Get console."""
        return self._console

    @property
    def obbject_registry(self) -> Registry:
        """Get obbject registry."""
        return self._obbject_registry

    @property
    def prompt_session(self) -> Optional[PromptSession]:
        """Get prompt session."""
        return self._prompt_session

    def _get_prompt_session(self) -> Optional[PromptSession]:
        """Initialize prompt session."""
        try:
            if sys.stdin.isatty():
                prompt_session: Optional[PromptSession] = PromptSession(
                    history=CustomFileHistory(str(HIST_FILE_PROMPT))
                )
            else:
                prompt_session = None
        except Exception:
            prompt_session = None

        return prompt_session

    def is_local(self) -> bool:
        """Check if user is local."""
        return not bool(self.user.profile.hub_session)

    def reset(self) -> None:
        pass

    def max_obbjects_exceeded(self) -> bool:
        """Check if max obbjects exceeded."""
        return (
            len(self.obbject_registry.all) >= self.settings.N_TO_KEEP_OBBJECT_REGISTRY
        )
