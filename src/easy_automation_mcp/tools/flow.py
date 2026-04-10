"""YAML-based automation flow execution tool for Easy Automation MCP."""

import time
from typing import Any

import keyboard as _keyboard
import mouse as _mouse
import pyautogui
import yaml
from pydantic import Field, ValidationError

from .._app import mcp
from .._state import RecordingSession, get_capture_dir, mouse_held, save_screenshot
from .flow_schema import AnyStep, FlowDefinition, FlowStep, RepeatStep


def _run_action(action: str, params: dict) -> dict[str, Any]:
    """Execute a single named action and return a result dict with a 'status' key.

    This is a low-level dispatcher used internally by execute_flow().
    Supported action names mirror the individual MCP tool names.
    """
    try:
        if action == "wait":
            seconds = float(params.get("seconds", 1.0))
            time.sleep(seconds)
            return {"status": "success", "message": f"Waited {seconds}s"}

        elif action == "get_screen_size":
            return {"status": "success", "message": f"Screen size: {pyautogui.size()}"}

        elif action == "get_mouse_position":
            pos = pyautogui.position()
            return {"status": "success", "message": f"Mouse position: ({pos.x}, {pos.y})"}

        elif action == "move_mouse":
            x, y = int(params["x"]), int(params["y"])
            pyautogui.moveTo(x, y)
            return {"status": "success", "message": f"Mouse moved to ({x}, {y})"}

        elif action == "click":
            held = [b for b, v in mouse_held.items() if v]
            if held:
                return {"status": "error", "message": f"Cannot click while {held} held"}
            pyautogui.click()
            return {"status": "success", "message": "Clicked at current position"}

        elif action == "double_click":
            held = [b for b, v in mouse_held.items() if v]
            if held:
                return {"status": "error", "message": f"Cannot double-click while {held} held"}
            pyautogui.doubleClick()
            return {"status": "success", "message": "Double-clicked at current position"}

        elif action == "triple_click":
            held = [b for b, v in mouse_held.items() if v]
            if held:
                return {"status": "error", "message": f"Cannot triple-click while {held} held"}
            pyautogui.tripleClick()
            return {"status": "success", "message": "Triple-clicked at current position"}

        elif action == "hold_mouse_button":
            button = params.get("button", "left")
            if button not in ("left", "middle", "right"):
                return {"status": "error", "message": f"Invalid button: '{button}'"}
            if mouse_held[button]:
                return {"status": "error", "message": f"'{button}' button is already held"}
            pyautogui.mouseDown(button=button)
            mouse_held[button] = True
            return {"status": "success", "message": f"Holding '{button}' button"}

        elif action == "release_mouse_button":
            button = params.get("button", "left")
            if button not in ("left", "middle", "right"):
                return {"status": "error", "message": f"Invalid button: '{button}'"}
            if not mouse_held[button]:
                return {"status": "error", "message": f"'{button}' button is not currently held"}
            pyautogui.mouseUp(button=button)
            mouse_held[button] = False
            return {"status": "success", "message": f"Released '{button}' button"}

        elif action == "drag_to":
            x, y = int(params["x"]), int(params["y"])
            duration = float(params.get("duration", 0.5))
            button = params.get("button", "left")
            if button not in ("left", "middle", "right"):
                return {"status": "error", "message": f"Invalid button: '{button}'"}
            if mouse_held[button]:
                return {"status": "error", "message": f"'{button}' button is already held"}
            pyautogui.dragTo(x, y, duration=duration, button=button)
            return {"status": "success", "message": f"Dragged to ({x}, {y})"}

        elif action == "scroll_up":
            clicks = int(params.get("clicks", 3))
            _mouse.wheel(clicks)
            return {"status": "success", "message": f"Scrolled up {clicks} step(s)"}

        elif action == "scroll_down":
            clicks = int(params.get("clicks", 3))
            _mouse.wheel(-clicks)
            return {"status": "success", "message": f"Scrolled down {clicks} step(s)"}

        elif action == "press_key":
            key = str(params["key"])
            _keyboard.press_and_release(key)
            return {"status": "success", "message": f"Pressed key: {key}"}

        elif action == "press_hotkey":
            keys = list(params["keys"])
            _keyboard.send("+".join(keys))
            return {"status": "success", "message": f"Pressed hotkey: {' + '.join(keys)}"}

        elif action == "type_text":
            text = str(params["text"])
            pyautogui.typewrite(text)
            return {"status": "success", "message": f"Typed {len(text)} character(s)"}

        elif action == "screenshot":
            path = save_screenshot("screenshot")
            return {"status": "success", "message": "Screenshot saved", "path": path}

        else:
            return {"status": "error", "message": f"Unknown action: '{action}'"}

    except pyautogui.FailSafeException:
        return {
            "status": "error",
            "message": "Failsafe triggered - mouse moved to a screen corner",
        }
    except KeyError as e:
        return {"status": "error", "message": f"Missing required parameter: {e}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def execute_flow(
    yaml_content: str = Field(description="YAML string defining the automation flow to execute"),
) -> dict[str, Any]:
    """Execute a sequence of GUI automation steps defined in YAML format.

    Use this tool to run multi-step automations reliably, with built-in support
    for error handling, retries, delays, looping, and per-step screenshots.

    --- YAML structure ---

    settings:           (optional)
      on_error: stop | continue | retry   # default: stop
      retry_count: int                    # default: 3  (used when on_error: retry)
      retry_delay: float                  # default: 1.0  seconds between retries
      default_wait: float                 # default: 0.0  seconds to wait after each step
      record: bool                        # default: false  record the screen during the flow (requires ffmpeg)
      record_fps: int                     # default: 30  frames per second for the recording

    steps:
      - action: <action_name>             # required — see supported actions below
        params:                           # action-specific parameters
          key: value
        id: <string>                      # optional label shown in results
        comment: <string>                 # ignored; human-readable note
        wait_after: <float>              # overrides default_wait for this step
        on_error: stop|continue|retry    # overrides global on_error for this step
        capture: true|false              # save a screenshot after this step

    --- Supported actions ---

    Screen / info:
      get_screen_size, get_mouse_position, screenshot

    Mouse:
      move_mouse        params: {x, y}
      click
      double_click
      triple_click
      drag_to           params: {x, y, duration (default 0.5), button (default left)}
      hold_mouse_button params: {button (default left)}
      release_mouse_button params: {button (default left)}
      scroll_up         params: {clicks (default 3)}
      scroll_down       params: {clicks (default 3)}

    Keyboard:
      press_key         params: {key}
      press_hotkey      params: {keys: [key1, key2, ...]}
      type_text         params: {text}

    Flow control (not MCP tools):
      wait              params: {seconds}
      repeat            count: int
                        steps: [...]   (max 1 level of nesting)

    --- Example ---

    settings:
      on_error: stop
      default_wait: 0.5

    steps:
      - action: move_mouse
        params: {x: 100, y: 200}
      - action: click
      - action: type_text
        params: {text: "hello"}
      - action: press_key
        params: {key: enter}
      - action: screenshot
        id: after_submit
    """
    # --- Parse YAML ---
    try:
        raw = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return {"status": "error", "message": f"Invalid YAML: {e}"}

    if not isinstance(raw, dict):
        return {"status": "error", "message": "YAML root must be a mapping"}

    # --- Validate with Pydantic ---
    try:
        flow_def = FlowDefinition.model_validate(raw)
    except ValidationError as e:
        return {"status": "error", "message": f"Invalid flow definition:\n{e}"}

    settings = flow_def.settings

    # --- Start recording (if requested) ---
    recording: RecordingSession | None = None
    recording_path: str | None = None
    recording_error: str | None = None
    if settings.record:
        recording = RecordingSession(fps=settings.record_fps)
        recording.start()

    # --- Execute steps ---
    step_results: list[dict[str, Any]] = []
    captures: list[str] = []
    total_executed = 0
    total_failed = 0
    aborted = False

    def run_step(step: AnyStep, depth: int = 0) -> dict[str, Any]:
        nonlocal total_executed, total_failed, aborted

        step_id = step.id or f"step_{total_executed + total_failed + 1}"
        step_on_error = step.on_error or settings.on_error

        # --- RepeatStep ---
        if isinstance(step, RepeatStep):
            iterations: list[list[dict[str, Any]]] = []
            for _ in range(step.count):
                if aborted:
                    break
                iter_results: list[dict[str, Any]] = []
                for sub_step in step.steps:
                    if aborted:
                        break
                    iter_results.append(run_step(sub_step, depth=1))
                iterations.append(iter_results)
            return {
                "id": step_id,
                "action": "repeat",
                "count": step.count,
                "status": "success",
                "iterations": iterations,
            }

        # --- FlowStep ---
        assert isinstance(step, FlowStep)
        wait = step.wait_after if step.wait_after is not None else settings.default_wait
        attempts = settings.retry_count if step_on_error == "retry" else 1

        action_result: dict[str, Any] = {"status": "error", "message": "not executed"}
        for attempt in range(attempts):
            action_result = _run_action(step.action, step.params)
            if action_result["status"] == "success":
                break
            if attempt < attempts - 1:
                time.sleep(settings.retry_delay)

        result: dict[str, Any] = {
            "id": step_id,
            "action": step.action,
            "status": action_result["status"],
            "message": action_result.get("message", ""),
        }
        if "path" in action_result:
            result["path"] = action_result["path"]
            captures.append(action_result["path"])

        if action_result["status"] == "success":
            total_executed += 1
        else:
            total_failed += 1
            if step_on_error == "stop":
                aborted = True

        if step.capture and not aborted:
            try:
                cap_path = save_screenshot(step_id)
                captures.append(cap_path)
                result["capture_path"] = cap_path
            except Exception as e:
                result["capture_error"] = str(e)

        if wait > 0 and not aborted:
            time.sleep(wait)

        return result

    for step in flow_def.steps:
        if aborted:
            break
        step_results.append(run_step(step))

    # --- Stop recording ---
    if recording is not None:
        try:
            recording_path = recording.stop()
        except Exception as e:
            recording_error = str(e)

    if total_failed == 0:
        status = "success"
    elif aborted:
        status = "error"
    else:
        status = "partial"

    result: dict[str, Any] = {
        "status": status,
        "steps_executed": total_executed,
        "steps_failed": total_failed,
        "aborted": aborted,
        "capture_dir": str(get_capture_dir()),
        "captures": captures,
        "step_results": step_results,
    }
    if recording_path is not None:
        result["recording_path"] = recording_path
    if recording_error is not None:
        result["recording_error"] = recording_error
    return result
