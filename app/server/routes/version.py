from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_version,
    delete_version,
    retrieve_version,
    retrieve_versions,
    update_version,
)
from app.server.models.version import (
    ErrorResponseModel,
    ResponseModel,
    VersionSchema,
    UpdateVersionModel,
)

router = APIRouter()

@router.post("/", response_description="Version data added into the database")
async def add_version_data(version: VersionSchema = Body(...)):
    version = jsonable_encoder(version)
    new_version = await add_version(version)
    return ResponseModel(new_version, "Version added successfully.")

@router.get("/", response_description="Versions retrieved")
async def get_versions():
    versions = await retrieve_versions()
    if versions:
        return ResponseModel(versions, "Versions data retrieved successfully")
    return ResponseModel(versions, "Empty list returned")


@router.get("/{id}", response_description="Version data retrieved")
async def get_version_data(id):
    version = await retrieve_version(id)
    if version:
        return ResponseModel(version, "Version data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "version doesn't exist.")

@router.put("/{id}")
async def update_version_data(id: str, req: UpdateVersionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_version = await update_version(id, req)
    if updated_version:
        return ResponseModel(
            "version with ID: {} name update is successful".format(id),
            "version name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the version data.",
    )

@router.delete("/{id}", response_description="Version data deleted from the database")
async def delete_version_data(id: str):
    deleted_version = await delete_version(id)
    if deleted_version:
        return ResponseModel(
            "version with ID: {} removed".format(id), "version deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Version with id {0} doesn't exist".format(id)
    )