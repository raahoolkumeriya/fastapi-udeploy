from fastapi import FastAPI

from app.server.routes.version import router as VersionRouter

app = FastAPI()

app.include_router(VersionRouter, tags=["Version"], prefix="/version")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Udeloy Version app!"}