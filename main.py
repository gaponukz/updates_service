from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from src.builds_storage import BuildsStorage
from src.upload.service import UploadService
from src.versoins_usecase.service import VersionsUsecase

from src import entities
from src import dto

app = FastAPI()
builds_storage = BuildsStorage("versions.json")
upload_service = UploadService(builds_storage, "versions")
version_usecase = VersionsUsecase(builds_storage)

@app.post("/upload_files")
async def on_upload_files(version: str, file: UploadFile) -> entities.Build:
    _version = entities.Version.from_string(version)
    build = entities.Build(str(version), f"versions/{file.filename}")
    
    await upload_service.add(file, _version)

    return build

@app.get("/get_versions")
async def on_get_current_version() -> dto.AllVersionDto:
    return dto.AllVersionDto(
        current=version_usecase.get_current_version(),
        awiable=version_usecase.get_sorted_versions()
    )

@app.get("/download")
async def root(version: str) -> FileResponse:
    return FileResponse(f"path/to/{version}.zip", media_type="application/zip", filename="main.zip")
