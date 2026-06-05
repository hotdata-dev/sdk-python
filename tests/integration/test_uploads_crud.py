"""Scenario: uploads_crud.

Upload a small file via upload_file, then confirm it appears in list_uploads.
There is no delete-upload endpoint, so the upload is not torn down in-test —
orphaned `sdkci` uploads are reclaimed by the nightly sweep. UploadInfo carries
no name field, so we identify the upload by the id returned from upload_file.
"""

from __future__ import annotations

from hotdata.api.uploads_api import UploadsApi


def test_uploads_crud(uploads_api: UploadsApi) -> None:
    body = b"col_a,col_b\n1,2\n3,4\n"

    uploaded = uploads_api.upload_file(body=body, _content_type="text/csv")
    assert uploaded.id
    assert uploaded.size_bytes == len(body)

    listing = uploads_api.list_uploads()
    match = next((u for u in listing.uploads if u.id == uploaded.id), None)
    assert match is not None, f"upload {uploaded.id} not in list_uploads"
    assert match.size_bytes == len(body)
