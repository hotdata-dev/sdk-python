# ColumnDefinition

Column type specification - either a simple type string or detailed spec with properties.  Simple form: `\"VARCHAR\"`, `\"INT\"`, `\"DATE\"` Detailed form: `{ \"type\": \"DECIMAL\", \"precision\": 10, \"scale\": 2 }`

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**geometry_type** | **object** | Geometry type for GEOMETRY/GEOGRAPHY columns. E.g., \&quot;Point\&quot;, \&quot;LineString\&quot;, \&quot;Polygon\&quot;, \&quot;MultiPoint\&quot;, \&quot;MultiLineString\&quot;, \&quot;MultiPolygon\&quot;, \&quot;GeometryCollection\&quot;, or \&quot;Geometry\&quot; (any). | [optional] 
**precision** | **object** | Precision for DECIMAL type (1-38) | [optional] 
**scale** | **object** | Scale for DECIMAL type | [optional] 
**srid** | **object** | Spatial Reference System Identifier for GEOMETRY/GEOGRAPHY types. Common values: 4326 (WGS84), 3857 (Web Mercator). | [optional] 
**type** | **str** | The data type name (e.g., \&quot;DECIMAL\&quot;, \&quot;TIMESTAMP\&quot;, \&quot;GEOMETRY\&quot;) | 

## Example

```python
from hotdata.models.column_definition import ColumnDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnDefinition from a JSON string
column_definition_instance = ColumnDefinition.from_json(json)
# print the JSON string representation of the object
print(ColumnDefinition.to_json())

# convert the object into a dict
column_definition_dict = column_definition_instance.to_dict()
# create an instance of ColumnDefinition from a dict
column_definition_from_dict = ColumnDefinition.from_dict(column_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


