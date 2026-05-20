#!/usr/bin/env python3
"""Re-apply ApiClient.close() after OpenAPI regeneration."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def patch_rest_client() -> None:
    path = ROOT / "hotdata" / "rest.py"
    src = path.read_text()
    needle = "            self.pool_manager = urllib3.PoolManager(**pool_args)\n\n    def request("
    insert = (
        "            self.pool_manager = urllib3.PoolManager(**pool_args)\n\n"
        "    def close(self) -> None:\n"
        "        if self.pool_manager is not None:\n"
        "            self.pool_manager.clear()\n\n"
        "    def request("
    )
    if "def close(self) -> None:" in src and "pool_manager.clear()" in src:
        return
    if needle not in src:
        sys.exit(f"Failed to patch {path}: RESTClientObject anchor not found")
    path.write_text(src.replace(needle, insert, 1))


def patch_api_client() -> None:
    path = ROOT / "hotdata" / "api_client.py"
    src = path.read_text()
    needle = (
        "    def __enter__(self):\n"
        "        return self\n\n"
        "    def __exit__(self, exc_type, exc_value, traceback):\n"
        "        pass\n"
    )
    replacement = (
        "    def __enter__(self):\n"
        "        return self\n\n"
        "    def close(self) -> None:\n"
        "        if self.rest_client is not None:\n"
        "            self.rest_client.close()\n\n"
        "    def __exit__(self, exc_type, exc_value, traceback):\n"
        "        self.close()\n"
    )
    if "def close(self) -> None:" in src and "self.rest_client.close()" in src:
        return
    if needle not in src:
        sys.exit(f"Failed to patch {path}: ApiClient context manager anchor not found")
    path.write_text(src.replace(needle, replacement, 1))


def main() -> None:
    patch_rest_client()
    patch_api_client()


if __name__ == "__main__":
    main()
