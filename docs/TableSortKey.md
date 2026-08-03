# TableSortKey

One key of a table's sort order.  Rows are written in this order, which keeps the values in each file within a narrow range and lets queries filtering on those columns skip files entirely. Most useful on columns you filter by ranges, such as a timestamp.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** |  | 
**direction** | **str** | &#x60;asc&#x60; (the default) or &#x60;desc&#x60;. | [optional] 
**nulls** | **str** | Where nulls are placed: &#x60;first&#x60; or &#x60;last&#x60;. Defaults to the SQL default for the chosen direction. | [optional] 

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


