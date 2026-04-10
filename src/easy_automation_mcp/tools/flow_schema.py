"""Pydantic models for YAML-based automation flow definitions.

These models validate and parse the YAML passed to execute_flow().
All field types and constraints are enforced at parse time, before any
automation steps are executed.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class FlowSettings(BaseModel):
    """Global settings that apply to every step in the flow unless overridden."""

    on_error: Literal["stop", "continue", "retry"] = "stop"
    """How to handle a step failure.

    - stop:     Abort the flow immediately (default).
    - continue: Log the failure and move on to the next step.
    - retry:    Retry the step up to retry_count times before failing.
    """

    retry_count: int = Field(default=3, ge=1)
    """Maximum number of attempts when on_error is 'retry'."""

    retry_delay: float = Field(default=1.0, ge=0.0)
    """Seconds to wait between retry attempts."""

    default_wait: float = Field(default=0.0, ge=0.0)
    """Seconds to wait after each step completes (unless overridden by wait_after)."""

    record: bool = False
    """If true, record the screen during the entire flow and save as an MP4 file."""

    record_fps: int = Field(default=30, ge=1)
    """Frames per second for the recording (default: 30)."""


class FlowStep(BaseModel):
    """A single automation action to execute."""

    action: str
    """Name of the action to run (e.g. 'click', 'type_text', 'move_mouse')."""

    params: dict[str, Any] = Field(default_factory=dict)
    """Action-specific parameters (e.g. {x: 100, y: 200} for move_mouse)."""

    id: str | None = None
    """Optional human-readable label used in result logs."""

    comment: str | None = None
    """Ignored at runtime; intended as a human-readable note in the YAML."""

    wait_after: float | None = Field(default=None, ge=0.0)
    """Seconds to wait after this step. Overrides settings.default_wait."""

    on_error: Literal["stop", "continue", "retry"] | None = None
    """Error handling for this step. Overrides settings.on_error when set."""

    capture: bool = False
    """If true, save a screenshot to the capture directory after this step."""


class RepeatStep(BaseModel):
    """A loop construct that repeats a list of steps a fixed number of times.

    Nesting RepeatStep inside another RepeatStep is not supported.
    """

    action: Literal["repeat"]
    count: int = Field(default=1, ge=1)
    """Number of times to repeat the inner steps."""

    steps: list[FlowStep] = Field(default_factory=list)
    """Steps to execute on each iteration. Only FlowStep is allowed here (no nesting)."""

    id: str | None = None
    on_error: Literal["stop", "continue", "retry"] | None = None


# Pydantic tries Union members left to right.
# RepeatStep matches only when action == "repeat"; FlowStep matches everything else.
AnyStep = RepeatStep | FlowStep


class FlowDefinition(BaseModel):
    """Top-level automation flow definition parsed from YAML.

    Expected YAML structure::

        settings:           # optional
          on_error: stop
          retry_count: 3
          retry_delay: 1.0
          default_wait: 0.5

        steps:
          - action: move_mouse
            params: {x: 100, y: 200}
          - action: click
          - action: repeat
            count: 3
            steps:
              - action: press_key
                params: {key: tab}
    """

    settings: FlowSettings = Field(default_factory=FlowSettings)
    steps: list[AnyStep] = Field(default_factory=list)
