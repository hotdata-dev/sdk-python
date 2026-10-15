"""Fail fast when a workspace-scoped request has no workspace to go to.

Most operations are scoped to a workspace through the ``X-Workspace-Id``
header (the ``WorkspaceId`` security scheme). The generated client simply
skips a scheme that has no configured value, so a ``Configuration`` built
without ``workspace_id`` sends the request anyway and the server answers with
a bare 404 that says nothing about what was missing.

:func:`ensure_workspace` runs before the request is sent (wired into
``ApiClient.update_params_for_auth`` by ``scripts/patch_workspace_guard.py``)
and raises :class:`MissingWorkspaceError` naming the constructor argument and
the environment variable. Operations whose security does not list
``WorkspaceId`` (workspace management itself) are unaffected, as are calls
that supply the header explicitly or override auth per request.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

from hotdata.exceptions import ApiValueError

WORKSPACE_SCHEME = "WorkspaceId"
WORKSPACE_HEADER = "X-Workspace-Id"


class MissingWorkspaceError(ApiValueError):
    """Raised before sending a workspace-scoped request when no workspace id
    is configured.

    Pass ``workspace_id=`` to :class:`hotdata.Configuration`, set the
    ``HOTDATA_WORKSPACE`` environment variable, or send the ``X-Workspace-Id``
    header explicitly for the call.
    """

    def __init__(self, resource_path: str, method: str) -> None:
        self.resource_path = resource_path
        self.method = method
        super().__init__(
            f"{method} {resource_path} is scoped to a workspace but no workspace id "
            "is configured. Pass workspace_id=... to hotdata.Configuration(...), "
            "set the HOTDATA_WORKSPACE environment variable, or send the "
            f"{WORKSPACE_HEADER} header explicitly (_headers=...)."
        )


def ensure_workspace(
    configuration: Any,
    auth_settings: Optional[Iterable[str]],
    headers: Optional[Mapping[str, Any]],
    resource_path: str,
    method: str,
    request_auth: Optional[Mapping[str, Any]] = None,
) -> None:
    """Raise :class:`MissingWorkspaceError` if the operation needs a workspace
    id and none would be sent.

    :param configuration: The client's :class:`hotdata.Configuration`.
    :param auth_settings: The operation's security scheme names.
    :param headers: Header params already assembled for the request.
    :param request_auth: A per-request auth override; when given the
        configuration is bypassed entirely, so the check is skipped.
    """
    if request_auth:
        return
    if not auth_settings or WORKSPACE_SCHEME not in auth_settings:
        return
    if headers and any(
        str(name).lower() == WORKSPACE_HEADER.lower() for name in headers
    ):
        return
    settings = configuration.auth_settings()
    scheme = settings.get(WORKSPACE_SCHEME) if settings else None
    if scheme and scheme.get("value"):
        return
    raise MissingWorkspaceError(resource_path, method)


__all__ = [
    "WORKSPACE_HEADER",
    "WORKSPACE_SCHEME",
    "MissingWorkspaceError",
    "ensure_workspace",
]
