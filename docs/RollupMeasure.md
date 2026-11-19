# RollupMeasure

One measure of a rollup declaration.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**centroids** | **int** | For &#x60;approx_percentile&#x60; only: the summary&#39;s accuracy, as the &#x60;centroids&#x60; argument of &#x60;approx_percentile_cont&#x60;. Defaults to 100, at most 1000; a query uses the rollup only with the same value (100 when it omits one). | [optional] 
**column** | **str** | Column to aggregate. Required for every kind except &#x60;count&#x60;, which counts all rows when it is omitted. | [optional] 
**kind** | **str** | The aggregate a measure keeps.  - &#x60;count&#x60;: number of rows, or with a &#x60;column&#x60;, rows where it is not null. - &#x60;sum&#x60;, &#x60;min&#x60;, &#x60;max&#x60;: that aggregate of &#x60;column&#x60;. - &#x60;numeric&#x60;: &#x60;count&#x60;, &#x60;sum&#x60;, &#x60;min&#x60; and &#x60;max&#x60; of &#x60;column&#x60;, enough to answer   &#x60;count&#x60;, &#x60;sum&#x60;, &#x60;avg&#x60;, &#x60;min&#x60; and &#x60;max&#x60; queries on it. &#x60;avg&#x60; of a decimal   column is always read from the table. - &#x60;approx_percentile&#x60;: a summary of &#x60;column&#x60; that answers   &#x60;approx_percentile_cont&#x60; and &#x60;approx_median&#x60; queries at any percentile.   Answers are approximate and can differ slightly from the same query on the   table. Much larger than other measures, and grows with &#x60;centroids&#x60;. | 

## Example

```python
from hotdata.models.rollup_measure import RollupMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of RollupMeasure from a JSON string
rollup_measure_instance = RollupMeasure.from_json(json)
# print the JSON string representation of the object
print(RollupMeasure.to_json())

# convert the object into a dict
rollup_measure_dict = rollup_measure_instance.to_dict()
# create an instance of RollupMeasure from a dict
rollup_measure_from_dict = RollupMeasure.from_dict(rollup_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


