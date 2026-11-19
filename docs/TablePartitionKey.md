# TablePartitionKey

A partition key. Rows with the same key value go into their own files, so queries that filter on the key read only the matching files.  Keys apply in order, and several can read one column. For one partition per month, use `year` and `month` on the same timestamp column: `month` alone puts every March of every year in one partition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** | Column the key reads. | 
**transform** | **str** | How the key is derived from the column: &#x60;identity&#x60; (the value itself), &#x60;year&#x60;, &#x60;month&#x60;, &#x60;day&#x60; or &#x60;hour&#x60;. | 

## Example

```python
from hotdata.models.table_partition_key import TablePartitionKey

# TODO update the JSON string below
json = "{}"
# create an instance of TablePartitionKey from a JSON string
table_partition_key_instance = TablePartitionKey.from_json(json)
# print the JSON string representation of the object
print(TablePartitionKey.to_json())

# convert the object into a dict
table_partition_key_dict = table_partition_key_instance.to_dict()
# create an instance of TablePartitionKey from a dict
table_partition_key_from_dict = TablePartitionKey.from_dict(table_partition_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


