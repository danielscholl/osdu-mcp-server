"""Error handling architecture for OSDU MCP Server.

This module implements the exception hierarchy as defined in ADR-004.
"""

from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any

from mcp import McpError
from mcp.types import ErrorData


class OSMCPError(Exception):
    """Base exception for OSDU MCP operations."""

    pass


class OSMCPAuthError(OSMCPError):
    """Authentication failures."""

    pass


class OSMCPAPIError(OSMCPError):
    """OSDU API communication errors."""

    def __init__(self, message: str, status_code: int | None = None):
        """Initialize API error with optional status code."""
        super().__init__(message)
        self.status_code = status_code


class OSMCPConfigError(OSMCPError):
    """Configuration validation errors."""

    pass


class OSMCPConnectionError(OSMCPError):
    """Network and connection errors."""

    pass


class OSMCPValidationError(OSMCPError):
    """Input validation errors."""

    pass


def handle_osdu_exceptions(
    func: Callable[..., Coroutine[Any, Any, Any]] | None = None,
    *,
    default_message: str = "OSDU operation failed",
) -> (
    Callable[..., Coroutine[Any, Any, Any]]
    | Callable[
        [Callable[..., Coroutine[Any, Any, Any]]],
        Callable[..., Coroutine[Any, Any, Any]],
    ]
):
    """Decorator to handle OSDU exceptions and convert them to MCP errors.

    Args:
        func: Async function to wrap (provided by decoration)
        default_message: Default error message if none provided

    Returns:
        Decorated async function that handles OSDU exceptions
    """

    def decorator(
        wrapped_func: Callable[..., Coroutine[Any, Any, Any]],
    ) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(wrapped_func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await wrapped_func(*args, **kwargs)
            except OSMCPAuthError as e:
                raise McpError(
                    ErrorData(code=401, message=f"Authentication error: {str(e)}")
                )
            except OSMCPAPIError as e:
                status = f" (HTTP {e.status_code})" if e.status_code else ""
                code = e.status_code if e.status_code else 500
                raise McpError(
                    ErrorData(code=code, message=f"OSDU API error{status}: {str(e)}")
                )
            except OSMCPConfigError as e:
                raise McpError(
                    ErrorData(code=400, message=f"Configuration error: {str(e)}")
                )
            except OSMCPConnectionError as e:
                raise McpError(
                    ErrorData(code=503, message=f"Connection error: {str(e)}")
                )
            except OSMCPValidationError as e:
                raise McpError(
                    ErrorData(code=400, message=f"Validation error: {str(e)}")
                )
            except OSMCPError as e:
                raise McpError(
                    ErrorData(code=500, message=f"{default_message}: {str(e)}")
                )
            except Exception as e:
                raise McpError(
                    ErrorData(
                        code=500,
                        message=f"Unexpected error in OSDU operation: {str(e)}",
                    )
                )

        return wrapper

    if func is None:
        # Called with parameters: @handle_osdu_exceptions(default_message="...")
        return decorator
    else:
        # Called without parameters: @handle_osdu_exceptions
        return decorator(func)
