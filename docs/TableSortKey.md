# TableSortKey

A sort key. Rows are written in this order, so queries that filter on these columns can skip files. Most useful on columns filtered by range, such as a timestamp.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** | Column to sort by. | 
**direction** | **str** | &#x60;asc&#x60; (default) or &#x60;desc&#x60;. Null in a response when it was not set. | [optional] 
**nulls** | **str** | Where nulls go: &#x60;first&#x60; or &#x60;last&#x60;. Defaults to &#x60;last&#x60; for &#x60;asc&#x60; and &#x60;first&#x60; for &#x60;desc&#x60;; null in a response when it was not set. | [optional] 

## Example

```python
from hotdata.models.table_sort_key import TableSortKey

# TODO update the JSON string below
json = "{}"
# create an instance of TableSortKey from a JSON string
table_sort_key_instance = TableSortKey.from_json(json)
# print the JSON string representation of the object
print(TableSortKey.to_json())

# convert the object into a dict
table_sort_key_dict = table_sort_key_instance.to_dict()
# create an instance of TableSortKey from a dict
table_sort_key_from_dict = TableSortKey.from_dict(table_sort_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


