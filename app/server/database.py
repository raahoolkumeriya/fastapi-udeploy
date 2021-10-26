import motor.motor_asyncio
import os
from bson.objectid import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_ATLAS_CONN"])
database = client.Udeploy
version_collection = database.get_collection("createversion")


# helpers
def version_helper(version) -> dict:
    return {
        "id": str(version["_id"]),
        "artifact_name": version["artifact_name"],
        "version_name": version["version_name"]
     }

# Retrieve all versions present in the database
async def retrieve_versions():
    versions = []
    async for version in version_collection.find():
        versions.append(version_helper(version))
    return versions


# Add a new version into to the database
async def add_version(version_data: dict) -> dict:
    version = await version_collection.insert_one(version_data)
    new_version = await version_collection.find_one({"_id": version.inserted_id})
    return version_helper(new_version)


# Retrieve a version with a matching ID
async def retrieve_version(id: str) -> dict:
    version = await version_collection.find_one({"_id": ObjectId(id)})
    if version:
        return version_helper(version)


# Update a version with a matching ID
async def update_version(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    version = await version_collection.find_one({"_id": ObjectId(id)})
    if version:
        updated_version = await version_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_version:
            return True
        return False

# Delete a version from the database
async def delete_version(id: str):
    version = await version_collection.find_one({"_id": ObjectId(id)})
    if version:
        await version_collection.delete_one({"_id": ObjectId(id)})
        return True