from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from src import entities
from src import dto

app = FastAPI()

@app.get("/upload_files")
async def on_upload_files(file: UploadFile) -> entities.Version:
    return entities.Version("0.0.1", "v0.0.1")

@app.get("/get_versions")
async def on_get_current_version() -> dto.AllVersionDto:
    return dto.AllVersionDto("0.0.1", [])

@app.get("/download")
async def root(version: str) -> FileResponse:
    return FileResponse(f"path/to/{version}.zip", media_type="application/zip", filename="main.zip")
