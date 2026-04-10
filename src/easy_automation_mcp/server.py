"""Easy Automation MCP server.

Imports the FastMCP instance and all tool modules. Each tool module registers
its tools via @mcp.tool() decorators as a side effect of being imported.
"""

from ._app import mcp
from .tools import flow, keyboard, mouse, screen

__all__ = ["mcp", "flow", "keyboard", "mouse", "screen"]
