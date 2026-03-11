# This client is a minimal scaffold. It will be replaced by auto-generated
# code from the HotData OpenAPI spec via the regenerate workflow.

from __future__ import annotations

import httpx


class HotdataClient:
    """Minimal HotData API client."""

    def __init__(
        self,
        api_token: str,
        workspace_id: str,
        base_url: str = "https://api.hotdata.dev",
    ) -> None:
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_token}",
                "X-Workspace-Id": workspace_id,
            },
        )

    def health(self) -> httpx.Response:
        return self._client.get("/health")

    def __enter__(self) -> HotdataClient:
        return self

    def __exit__(self, *args: object) -> None:
        self._client.close()

    def close(self) -> None:
        self._client.close()
