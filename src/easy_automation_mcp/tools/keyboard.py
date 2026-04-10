"""Keyboard control tools for Easy Automation MCP."""


import keyboard as _keyboard
import pyautogui
from pydantic import Field

from .._app import mcp

# Complete list of key names accepted by press_key() and press_hotkey().
_AVAILABLE_KEYS: list[str] = (
    list("abcdefghijklmnopqrstuvwxyz")
    + [str(i) for i in range(10)]
    + [f"f{i}" for i in range(1, 25)]
    + [
        "enter",
        "return",
        "space",
        "tab",
        "backspace",
        "delete",
        "escape",
        "esc",
        "insert",
        "home",
        "end",
        "page up",
        "page down",
        "up",
        "down",
        "left",
        "right",
        "ctrl",
        "left ctrl",
        "right ctrl",
        "alt",
        "left alt",
        "right alt",
        "shift",
        "left shift",
        "right shift",
        "windows",
        "left windows",
        "right windows",
        "caps lock",
        "num lock",
        "scroll lock",
        "print screen",
        "pause",
        "num 0",
        "num 1",
        "num 2",
        "num 3",
        "num 4",
        "num 5",
        "num 6",
        "num 7",
        "num 8",
        "num 9",
        "num *",
        "num +",
        "num -",
        "num .",
        "num /",
        "`",
        "-",
        "=",
        "[",
        "]",
        "\\",
        ";",
        "'",
        ",",
        ".",
        "/",
    ]
)


@mcp.tool()
def list_available_keys() -> list[str]:
    """Return all key names that can be used with press_key() and press_hotkey().

    Use this to look up the exact string to pass when you are unsure of a key name
    (e.g., 'page up', 'left ctrl', 'num 0').
    """
    return _AVAILABLE_KEYS


@mcp.tool()
def press_key(
    key: str = Field(
        description="Name of the key to press and release (e.g. 'enter', 'tab', 'f5', 'a'). "
                    "Call list_available_keys() to see all valid names."
    ),
) -> dict[str, str]:
    """Press and release a single keyboard key."""
    try:
        _keyboard.press_and_release(key)
        return {"status": "success", "message": f"Pressed key: {key}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to press key '{key}': {e}"}


@mcp.tool()
def press_hotkey(
    keys: list[str] = Field(
        description="Ordered list of key names to press simultaneously. "
                    "Example: ['ctrl', 'c'] for Copy, ['ctrl', 'shift', 'esc'] for Task Manager."
    ),
) -> dict[str, str]:
    """Press multiple keys simultaneously as a keyboard shortcut.

    Keys are pressed in list order and released together.
    Call list_available_keys() to see all valid key names.
    """
    try:
        _keyboard.send("+".join(keys))
        return {
            "status": "success",
            "message": f"Pressed hotkey: {' + '.join(keys)}",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to press hotkey {keys}: {e}"}


@mcp.tool()
def type_text(
    text: str = Field(description="The text string to type character by character"),
) -> dict[str, str]:
    """Type a string of characters as if entered from the keyboard.

    Each character is sent as individual key events using pyautogui.typewrite().
    Note: only printable ASCII characters are supported. For Unicode or special
    characters, use press_hotkey() or the clipboard instead.
    """
    try:
        pyautogui.typewrite(text)
        return {
            "status": "success",
            "message": f"Typed {len(text)} character(s)",
        }
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse moved to a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to type text: {e}"}
