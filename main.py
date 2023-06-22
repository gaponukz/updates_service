# uvicorn main:app --log-config log.ini
# docker run -d -p 8000:8000 -v database:/app/database updates-service
from fastapi import FastAPI, UploadFile
from fastapi import HTTPException, Depends
from fastapi.responses import FileResponse

from src.builds_storage import BuildsStorage
from src.upload.service import UploadService
from src.versoins_usecase.service import VersionsUsecase
from src.authentication.admin import admin_required

from src import entities
from src import errors
from src import dto

import logging

logging.basicConfig(
    filename="main.log",
    filemode="w",
    encoding="utf-8",
    level=logging.DEBUG
)

app = FastAPI()
builds_storage = BuildsStorage("database/versions.json")
upload_service = UploadService(builds_storage, "database/versions")
version_usecase = VersionsUsecase(builds_storage)

@app.post("/upload_files")
async def on_upload_files(
    version: str,
    file: UploadFile,
    description: str="",
    api_key: str = Depends(admin_required)
) -> entities.Build:
    _version = entities.Version.from_string(version)
    build = entities.Build(str(version), f"database/versions/{file.filename}", description)
    
    try:
        await upload_service.add(file, _version)

    except errors.BuildAlreadyExistsError as error:
        raise HTTPException(status_code=400, detail=f"{error.version} already exist")
    
    return build

@app.post("/set_current_version")
async def on_set_current_version(
        version: entities.VersionSymbol,
        api_key: str = Depends(admin_required)
    ):
    try:
        version_usecase.set_current_version(version)
    
    except errors.BuildNotFoundError as error:
        raise HTTPException(status_code=400, detail=f"{error.version} not found")

@app.get("/get_versions")
async def on_get_current_version(api_key: str = Depends(admin_required)) -> dto.AllVersionDto:
    return dto.AllVersionDto(
        current=version_usecase.get_current_version(),
        awiable=version_usecase.get_sorted_versions()
    )

@app.get("/download")
async def root() -> FileResponse:
    current = version_usecase.get_current_version()

    if current is None:
        raise HTTPException(status_code=500, detail=f"no selected version")
    
    build = builds_storage.get_by_version(current)

    return FileResponse(build.file_path, media_type="application/zip", filename="main.zip")
