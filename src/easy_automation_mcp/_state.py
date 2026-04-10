"""
Shared mutable state for Easy Automation MCP.

This module centralizes state that is shared across tool modules:
  - Mouse button hold state (to prevent invalid click sequences)
  - Screenshot capture directory
"""

from datetime import datetime
from pathlib import Path

import pyautogui

# Tracks which mouse buttons are currently held down via mouse_down().
# Used to prevent clicks while a button is held.
mouse_held: dict[str, bool] = {"left": False, "middle": False, "right": False}

# Directory where screenshots and flow captures are saved.
_capture_dir: Path = Path.home() / "Documents" / "Automation"


def set_capture_dir(path: Path) -> None:
    """Override the default screenshot save directory."""
    global _capture_dir
    _capture_dir = path


def get_capture_dir() -> Path:
    """Return the current screenshot save directory."""
    return _capture_dir


def _ensure_capture_dir() -> Path:
    """Create the capture directory if it does not exist, then return it."""
    _capture_dir.mkdir(parents=True, exist_ok=True)
    return _capture_dir


def save_screenshot(label: str = "") -> str:
    """Take a screenshot, save it to the capture directory, and return the file path.

    The filename format is: YYYYMMDD_HHMMSS_ffffff[_label].jpg
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name = f"{ts}_{label}.jpg" if label else f"{ts}.jpg"
    path = _ensure_capture_dir() / name
    img = pyautogui.screenshot()
    img.convert("RGB").save(str(path), format="JPEG", quality=85)
    return str(path)
