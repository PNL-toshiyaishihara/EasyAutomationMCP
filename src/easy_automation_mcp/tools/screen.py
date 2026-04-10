"""Screen and screenshot tools for Easy Automation MCP."""

import base64
import io

import pyautogui
from mcp.types import ImageContent

from .._app import mcp
from .._state import save_screenshot  # noqa: F401 - re-exported for use in flow.py


@mcp.tool()
def get_screen_size() -> dict[str, str]:
    """Return the screen resolution as width and height in pixels.

    Useful for calculating coordinates before moving or clicking the mouse.
    """
    size = pyautogui.size()
    return {"status": "success", "message": f"Screen size: {size.width}x{size.height}px"}


@mcp.tool()
def screenshot() -> ImageContent | dict[str, str]:
    """Capture a screenshot of the entire screen and return it as a JPEG image.

    The image is returned inline as Base64-encoded data so the caller can view
    the current state of the screen without writing a file to disk.
    """
    try:
        buffer = io.BytesIO()
        img = pyautogui.screenshot()
        img.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)
        return ImageContent(
            type="image",
            data=base64.b64encode(buffer.getvalue()).decode(),
            mimeType="image/jpeg",
        )
    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse moved to a screen corner",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to capture screenshot: {e}"}
