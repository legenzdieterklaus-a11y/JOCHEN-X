"""Token-based application themes."""

from dataclasses import dataclass
from config.settings import ThemeMode


@dataclass(frozen=True, slots=True)
class ThemeTokens:
    """Colors, typography, spacing, icons, and animation timing for a theme."""
    background: str
    foreground: str
    surface: str
    accent: str
    font_family: str = "Segoe UI"
    spacing: int = 8
    icon_size: int = 20
    animation_ms: int = 160


LIGHT = ThemeTokens("#f7f8fa", "#17202a", "#ffffff", "#0067c0")
DARK = ThemeTokens("#1e1e1e", "#f1f1f1", "#292929", "#4da3ff")


class ThemeEngine:
    """Selects a theme and turns tokens into the Qt application stylesheet."""
    def select(self, mode: ThemeMode) -> ThemeTokens:
        """Resolve system mode conservatively to dark when Qt has no platform hint."""
        return LIGHT if mode is ThemeMode.LIGHT else DARK

    def stylesheet(self, tokens: ThemeTokens) -> str:
        """Create the complete base stylesheet from immutable design tokens."""
        return (f"QWidget {{ background: {tokens.background}; color: {tokens.foreground}; "
                f"font-family: '{tokens.font_family}'; }} QMainWindow {{ background: {tokens.background}; }} "
                f"QFrame#surface {{ background: {tokens.surface}; border-radius: {tokens.spacing}px; }}")
