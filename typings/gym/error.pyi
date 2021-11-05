"""
This type stub file was generated by pyright.
"""

class Error(Exception): ...

class Unregistered(Error):
    """Raised when the user requests an item from the registry that does
    not actually exist.
    """

    ...

class UnregisteredEnv(Unregistered):
    """Raised when the user requests an env from the registry that does
    not actually exist.
    """

    ...

class UnregisteredBenchmark(Unregistered):
    """Raised when the user requests an env from the registry that does
    not actually exist.
    """

    ...

class DeprecatedEnv(Error):
    """Raised when the user requests an env from the registry with an
    older version number than the latest env with the same name.
    """

    ...

class UnseedableEnv(Error):
    """Raised when the user tries to seed an env that does not support
    seeding.
    """

    ...

class DependencyNotInstalled(Error): ...

class UnsupportedMode(Exception):
    """Raised when the user requests a rendering mode not supported by the
    environment.
    """

    ...

class ResetNeeded(Exception):
    """When the monitor is active, raised when the user tries to step an
    environment that's already done.
    """

    ...

class ResetNotAllowed(Exception):
    """When the monitor is active, raised when the user tries to step an
    environment that's not yet done.
    """

    ...

class InvalidAction(Exception):
    """Raised when the user performs an action not contained within the
    action space
    """

    ...

class APIError(Error):
    def __init__(
        self, message=..., http_body=..., http_status=..., json_body=..., headers=...
    ) -> None: ...
    def __unicode__(self): ...
    def __str__(self) -> str: ...

class APIConnectionError(APIError): ...

class InvalidRequestError(APIError):
    def __init__(
        self, message, param, http_body=..., http_status=..., json_body=..., headers=...
    ) -> None: ...

class AuthenticationError(APIError): ...
class RateLimitError(APIError): ...
class VideoRecorderError(Error): ...
class InvalidFrame(Error): ...
class DoubleWrapperError(Error): ...
class WrapAfterConfigureError(Error): ...
class RetriesExceededError(Error): ...

class AlreadyPendingCallError(Exception):
    """
    Raised when `reset`, or `step` is called asynchronously (e.g. with
    `reset_async`, or `step_async` respectively), and `reset_async`, or
    `step_async` (respectively) is called again (without a complete call to
    `reset_wait`, or `step_wait` respectively).
    """

    def __init__(self, message, name) -> None: ...

class NoAsyncCallError(Exception):
    """
    Raised when an asynchronous `reset`, or `step` is not running, but
    `reset_wait`, or `step_wait` (respectively) is called.
    """

    def __init__(self, message, name) -> None: ...

class ClosedEnvironmentError(Exception):
    """
    Trying to call `reset`, or `step`, while the environment is closed.
    """

    ...

class CustomSpaceError(Exception):
    """
    The space is a custom gym.Space instance, and is not supported by
    `AsyncVectorEnv` with `shared_memory=True`.
    """

    ...
