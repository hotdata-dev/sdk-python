"""Scenario: datasets_crud.

Defined in www.hotdata.dev/api/test-scenarios.yaml — create, read, list,
update, and delete a dataset; assert 404 after delete.
"""

from __future__ import annotations

import pytest

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
            inline=InlineData(
                content="a,b\n1,2\n3,4\n",
                format="csv",
            ),
        )
    )


def test_datasets_crud(datasets_api: DatasetsApi, sdkci_name) -> None:
    label = sdkci_name("datasets-crud")
    new_label = f"{label}-renamed"
    created_id: str | None = None

    try:
        created = datasets_api.create_dataset(
            CreateDatasetRequest(label=label, source=_inline_csv_source())
        )
        created_id = created.id
        assert created.label == label
        assert created.id

        fetched = datasets_api.get_dataset(created.id)
        assert fetched.id == created.id
        assert fetched.label == label
        assert fetched.columns, "expected inferred columns from inline CSV"

        listing = datasets_api.list_datasets()
        assert any(d.id == created.id for d in listing.datasets), (
            f"newly created dataset {created.id} not present in list_datasets"
        )

        updated = datasets_api.update_dataset(
            created.id, UpdateDatasetRequest(label=new_label)
        )
        assert updated.label == new_label

        datasets_api.delete_dataset(created.id)
        created_id = None  # successful delete — skip teardown

        with pytest.raises(ApiException) as excinfo:
            datasets_api.get_dataset(created.id)
        assert excinfo.value.status == 404, (
            f"expected 404 after delete, got {excinfo.value.status}"
        )
    finally:
        if created_id is not None:
            try:
                datasets_api.delete_dataset(created_id)
            except ApiException:
                pass
