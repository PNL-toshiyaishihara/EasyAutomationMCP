# Importing each submodule triggers @mcp.tool() decorators and registers all tools.
from . import flow, keyboard, mouse, screen  # noqa: F401
