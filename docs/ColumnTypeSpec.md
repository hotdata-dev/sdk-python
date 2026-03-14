# ColumnTypeSpec

Detailed column type specification with optional properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**geometry_type** | **str** | Geometry type for GEOMETRY/GEOGRAPHY columns. E.g., \&quot;Point\&quot;, \&quot;LineString\&quot;, \&quot;Polygon\&quot;, \&quot;MultiPoint\&quot;, \&quot;MultiLineString\&quot;, \&quot;MultiPolygon\&quot;, \&quot;GeometryCollection\&quot;, or \&quot;Geometry\&quot; (any). | [optional] 
**precision** | **int** | Precision for DECIMAL type (1-38) | [optional] 
**scale** | **int** | Scale for DECIMAL type | [optional] 
**srid** | **int** | Spatial Reference System Identifier for GEOMETRY/GEOGRAPHY types. Common values: 4326 (WGS84), 3857 (Web Mercator). | [optional] 
**type** | **str** | The data type name (e.g., \&quot;DECIMAL\&quot;, \&quot;TIMESTAMP\&quot;, \&quot;GEOMETRY\&quot;) | 

## Example

```python
from hotdata.models.column_type_spec import ColumnTypeSpec

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnTypeSpec from a JSON string
column_type_spec_instance = ColumnTypeSpec.from_json(json)
# print the JSON string representation of the object
print(ColumnTypeSpec.to_json())

# convert the object into a dict
column_type_spec_dict = column_type_spec_instance.to_dict()
# create an instance of ColumnTypeSpec from a dict
column_type_spec_from_dict = ColumnTypeSpec.from_dict(column_type_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


