from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from src.verion_storage import VersionStorage
from src.upload.service import UploadService
from src import entities
from src import versions
from src import dto

app = FastAPI()
version_storage = VersionStorage("versions.txt")
upload_service = UploadService(version_storage, "versions")

@app.post("/upload_files")
async def on_upload_files(version: str, file: UploadFile) -> entities.Build:
    _version = versions.Version.from_string(version)
    build = entities.Build(str(version), f"versions/{file.filename}")
    
    await upload_service.add(file, _version)

    return build

@app.get("/get_versions")
async def on_get_current_version() -> dto.AllVersionDto:
    return dto.AllVersionDto("0.0.1", [])

@app.get("/download")
async def root(version: str) -> FileResponse:
    return FileResponse(f"path/to/{version}.zip", media_type="application/zip", filename="main.zip")
