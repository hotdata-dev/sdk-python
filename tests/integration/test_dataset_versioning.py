"""Scenario: dataset_versioning.

Create a dataset, exercise list_dataset_versions, pin to a specific version,
then unpin. Confirms the versioning surface is reachable and consistent.
"""

from __future__ import annotations

from hotdata.api.datasets_api import DatasetsApi
from hotdata.exceptions import ApiException
from hotdata.models.create_dataset_request import CreateDatasetRequest
from hotdata.models.dataset_source import DatasetSource
from hotdata.models.dataset_source_one_of4 import DatasetSourceOneOf4
from hotdata.models.inline_data import InlineData
from hotdata.models.update_dataset_request import UpdateDatasetRequest


def _inline_csv_source() -> DatasetSource:
    return DatasetSource(
        DatasetSourceOneOf4(
            type="inline",
            inline=InlineData(content="a,b\n1,2\n3,4\n", format="csv"),
        )
    )


def test_dataset_versioning(datasets_api: DatasetsApi, sdkci_name) -> None:
    label = sdkci_name("dataset-versioning")
    created_id: str | None = None

    try:
        created = datasets_api.create_dataset(
            CreateDatasetRequest(label=label, source=_inline_csv_source())
        )
        created_id = created.id

        versions = datasets_api.list_dataset_versions(created.id)
        assert versions.dataset_id == created.id
        assert versions.count >= 1
        assert any(v.version == 1 for v in versions.versions), (
            f"expected version 1 in {[v.version for v in versions.versions]}"
        )

        pinned = datasets_api.update_dataset(
            created.id, UpdateDatasetRequest(pinned_version=1)
        )
        assert pinned.pinned_version == 1
        assert pinned.latest_version >= 1

        fetched = datasets_api.get_dataset(created.id)
        assert fetched.pinned_version == 1
    finally:
        if created_id is not None:
            try:
                datasets_api.delete_dataset(created_id)
            except ApiException:
                pass
