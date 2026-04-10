"""Mouse control tools for Easy Automation MCP."""


import mouse as _mouse
import pyautogui
from pydantic import Field

from .._app import mcp
from .._state import mouse_held


@mcp.tool()
def get_mouse_position() -> dict[str, str]:
    """Return the current (x, y) position of the mouse cursor in screen pixels."""
    pos = pyautogui.position()
    return {"status": "success", "message": f"Mouse position: ({pos.x}, {pos.y})"}


@mcp.tool()
def move_mouse(
    x: int = Field(description="Target X coordinate in screen pixels"),
    y: int = Field(description="Target Y coordinate in screen pixels"),
) -> dict[str, str]:
    """Move the mouse cursor to the specified screen coordinates without clicking."""
    try:
        pyautogui.moveTo(x, y)
        return {"status": "success", "message": f"Mouse moved to ({x}, {y})"}
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse moved to a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to move mouse: {e}"}


@mcp.tool()
def click() -> dict[str, str]:
    """Click the left mouse button at the current cursor position.

    Fails if any mouse button is currently held down via hold_mouse_button().
    Call release_mouse_button() first to clear the held state.
    """
    held = [b for b, v in mouse_held.items() if v]
    if held:
        return {
            "status": "error",
            "message": f"Cannot click while {held} button(s) are held. Call release_mouse_button() first",
        }
    try:
        pyautogui.click()
        return {"status": "success", "message": "Clicked at current cursor position"}
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse is at a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to click: {e}"}


@mcp.tool()
def double_click() -> dict[str, str]:
    """Double-click the left mouse button at the current cursor position.

    Fails if any mouse button is currently held down via hold_mouse_button().
    """
    held = [b for b, v in mouse_held.items() if v]
    if held:
        return {
            "status": "error",
            "message": f"Cannot double-click while {held} button(s) are held. Call release_mouse_button() first",
        }
    try:
        pyautogui.doubleClick()
        return {"status": "success", "message": "Double-clicked at current cursor position"}
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse is at a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to double-click: {e}"}


@mcp.tool()
def triple_click() -> dict[str, str]:
    """Triple-click the left mouse button at the current cursor position.

    Commonly used to select an entire line or word in text editors.
    Fails if any mouse button is currently held down via hold_mouse_button().
    """
    held = [b for b, v in mouse_held.items() if v]
    if held:
        return {
            "status": "error",
            "message": f"Cannot triple-click while {held} button(s) are held. Call release_mouse_button() first",
        }
    try:
        pyautogui.tripleClick()
        return {"status": "success", "message": "Triple-clicked at current cursor position"}
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse is at a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to triple-click: {e}"}


@mcp.tool()
def hold_mouse_button(
    button: str = Field(
        default="left",
        description="Button to hold down: 'left', 'middle', or 'right'",
    ),
) -> dict[str, str]:
    """Press and hold a mouse button at the current cursor position.

    Use together with move_mouse() and release_mouse_button() to perform
    manual drag operations that require stopping at intermediate positions.
    For simple drags, prefer drag_to() instead.
    """
    if button not in ("left", "middle", "right"):
        return {
            "status": "error",
            "message": f"Invalid button '{button}'. Must be 'left', 'middle', or 'right'",
        }
    if mouse_held[button]:
        return {"status": "error", "message": f"'{button}' button is already held down"}
    try:
        pyautogui.mouseDown(button=button)
        mouse_held[button] = True
        return {"status": "success", "message": f"Holding down '{button}' mouse button"}
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse is at a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to hold mouse button: {e}"}


@mcp.tool()
def release_mouse_button(
    button: str = Field(
        default="left",
        description="Button to release: 'left', 'middle', or 'right'",
    ),
) -> dict[str, str]:
    """Release a mouse button that was previously held down via hold_mouse_button()."""
    if button not in ("left", "middle", "right"):
        return {
            "status": "error",
            "message": f"Invalid button '{button}'. Must be 'left', 'middle', or 'right'",
        }
    if not mouse_held[button]:
        return {
            "status": "error",
            "message": f"'{button}' button is not currently held down",
        }
    try:
        pyautogui.mouseUp(button=button)
        mouse_held[button] = False
        return {"status": "success", "message": f"Released '{button}' mouse button"}
    except pyautogui.FailSafeException:
        mouse_held[button] = False
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse is at a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to release mouse button: {e}"}


@mcp.tool()
def drag_to(
    x: int = Field(description="Target X coordinate to drag to"),
    y: int = Field(description="Target Y coordinate to drag to"),
    duration: float = Field(default=0.5, description="Duration of the drag movement in seconds"),
    button: str = Field(
        default="left",
        description="Mouse button to drag with: 'left', 'middle', or 'right'",
    ),
) -> dict[str, str]:
    """Drag the mouse from the current cursor position to the target coordinates.

    Presses the specified button, moves smoothly to (x, y) over the given
    duration, then releases the button. For complex multi-stop drags, use
    hold_mouse_button() / move_mouse() / release_mouse_button() instead.
    """
    if button not in ("left", "middle", "right"):
        return {
            "status": "error",
            "message": f"Invalid button '{button}'. Must be 'left', 'middle', or 'right'",
        }
    if mouse_held[button]:
        return {
            "status": "error",
            "message": f"'{button}' button is already held. Release it with release_mouse_button() first",
        }
    try:
        pyautogui.dragTo(x, y, duration=duration, button=button)
        return {"status": "success", "message": f"Dragged to ({x}, {y})"}
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse moved to a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to drag: {e}"}


@mcp.tool()
def scroll_up(
    clicks: int = Field(default=3, description="Number of scroll steps upward"),
) -> dict[str, str]:
    """Scroll the mouse wheel upward at the current cursor position."""
    try:
        _mouse.wheel(clicks)
        return {"status": "success", "message": f"Scrolled up {clicks} step(s)"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to scroll up: {e}"}


@mcp.tool()
def scroll_down(
    clicks: int = Field(default=3, description="Number of scroll steps downward"),
) -> dict[str, str]:
    """Scroll the mouse wheel downward at the current cursor position."""
    try:
        _mouse.wheel(-clicks)
        return {"status": "success", "message": f"Scrolled down {clicks} step(s)"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to scroll down: {e}"}
