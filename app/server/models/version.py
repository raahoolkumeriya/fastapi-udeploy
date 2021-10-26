from typing import Optional

from pydantic import BaseModel, Field


class VersionSchema(BaseModel):
    artifact_name: str = Field(...)
    version_name: str = Field(...)
   
    class Config:
        schema_extra = {
            "example": {
                "artifact_name": "DEPLOYME-10.0.0.1.tar.gz",
                "version_name": "10.0.0.1"
            }
        }


class UpdateVersionModel(BaseModel):
    artifact_name: Optional[str]
    version_name: Optional[str]
   
    class Config:
        schema_extra = {
            "example": {
                "artifact_name": "DEPLOYME-10.0.0.1.tar.gz",
                "version_name": "10.0.0.1"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}