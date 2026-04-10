import argparse
import os
from pathlib import Path

from ._state import set_capture_dir
from .server import mcp


def main():
    """Easy Automation MCP - Control the mouse and keyboard using MCP"""
    parser = argparse.ArgumentParser(description="Easy Automation MCP")
    parser.add_argument(
        "--capture-dir",
        type=str,
        default=None,
        help=(
            "Directory to save screenshots and captures. "
            "Overrides EASY_AUTOMATION_MCP_CAPTURE_DIR env var. "
            "Default: ~/Documents/Automation"
        ),
    )
    args, _ = parser.parse_known_args()

    capture_dir = args.capture_dir or os.environ.get("EASY_AUTOMATION_MCP_CAPTURE_DIR")
    if capture_dir:
        set_capture_dir(Path(capture_dir))

    mcp.run()


if __name__ == "__main__":
    main()
