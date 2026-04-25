"""Scenario: indexes_lifecycle.

Create a dataset, build a sorted index on one of its columns, list indexes,
then delete the index and clean up the dataset. Indexes are scoped to
(connection_id, schema, table); datasets surface table_name + schema_name so
we can target them directly.
"""

from __future__ import annotations

from hotdata.api.datasets_api import DatasetsApi
from hotdata.api.indexes_api import IndexesApi
from hotdata.exceptions import ApiException
from hotdata.models.create_dataset_request import CreateDatasetRequest
from hotdata.models.create_index_request import CreateIndexRequest
from hotdata.models.dataset_source import DatasetSource
from hotdata.models.inline_data import InlineData
from hotdata.models.inline_dataset_source import InlineDatasetSource


def _inline_csv_source() -> DatasetSource:
    return DatasetSource(
        InlineDatasetSource(
            inline=InlineData(content="a,b\n1,2\n3,4\n5,6\n", format="csv")
        )
    )


def test_indexes_lifecycle(
    datasets_api: DatasetsApi,
    indexes_api: IndexesApi,
    connection_id: str,
    sdkci_name,
) -> None:
    label = sdkci_name("indexes")
    index_name = sdkci_name("idx").replace("-", "_")  # index names tend to be SQL-ident-ish

    dataset_id: str | None = None
    index_created = False
    schema_name: str | None = None
    table_name: str | None = None

    try:
        dataset = datasets_api.create_dataset(
            CreateDatasetRequest(label=label, source=_inline_csv_source())
        )
        dataset_id = dataset.id
        schema_name = dataset.schema_name
        table_name = dataset.table_name

        created = indexes_api.create_index(
            connection_id=connection_id,
            var_schema=schema_name,
            table=table_name,
            create_index_request=CreateIndexRequest(
                index_name=index_name,
                columns=["a"],
                index_type="sorted",
            ),
        )
        index_created = True
        assert created.index_name == index_name
        assert "a" in created.columns

        listing = indexes_api.list_indexes(
            connection_id=connection_id,
            var_schema=schema_name,
            table=table_name,
        )
        assert any(i.index_name == index_name for i in listing.indexes), (
            f"index {index_name} not present after create"
        )
    finally:
        if index_created and schema_name and table_name:
            try:
                indexes_api.delete_index(
                    connection_id=connection_id,
                    var_schema=schema_name,
                    table=table_name,
                    index_name=index_name,
                )
            except ApiException:
                pass
        if dataset_id is not None:
            try:
                datasets_api.delete_dataset(dataset_id)
            except ApiException:
                pass
