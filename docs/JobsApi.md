# hotdata.JobsApi

All URIs are relative to *https://app.hotdata.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_job**](JobsApi.md#get_job) | **GET** /v1/jobs/{id} | Get job status
[**list_jobs**](JobsApi.md#list_jobs) | **GET** /v1/jobs | List jobs


# **get_job**
> JobStatusResponse get_job(id)

Get job status

Get the current status of a background job. Poll this endpoint to track job progress.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.job_status_response import JobStatusResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.JobsApi(api_client)
    id = 'id_example' # str | Job ID

    try:
        # Get job status
        api_response = api_instance.get_job(id)
        print("The response of JobsApi->get_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->get_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Job ID | 

### Return type

[**JobStatusResponse**](JobStatusResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Job status |  -  |
**404** | Job not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_jobs**
> ListJobsResponse list_jobs(job_type=job_type, status=status, limit=limit, offset=offset)

List jobs

List background jobs with optional filters by type and status.

### Example

* Bearer Authentication (BearerAuth):

```python
import hotdata
from hotdata.models.list_jobs_response import ListJobsResponse
from hotdata.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://app.hotdata.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = hotdata.Configuration(
    host = "https://app.hotdata.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = hotdata.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with hotdata.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hotdata.JobsApi(api_client)
    job_type = 'job_type_example' # str | Filter by job type (optional)
    status = 'status_example' # str | Filter by status (optional)
    limit = 56 # int | Max results (default 50) (optional)
    offset = 56 # int | Offset for pagination (optional)

    try:
        # List jobs
        api_response = api_instance.list_jobs(job_type=job_type, status=status, limit=limit, offset=offset)
        print("The response of JobsApi->list_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobsApi->list_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_type** | **str**| Filter by job type | [optional] 
 **status** | **str**| Filter by status | [optional] 
 **limit** | **int**| Max results (default 50) | [optional] 
 **offset** | **int**| Offset for pagination | [optional] 

### Return type

[**ListJobsResponse**](ListJobsResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of jobs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

