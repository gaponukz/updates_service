from typing import Annotated
from fastapi import FastAPI, UploadFile, Form
from fastapi import HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from src.builds_storage import BuildsStorage
from src.upload.service import UploadService
from src.delete.service import DeleteService
from src.versoins_usecase.service import VersionsUsecase
from src.authentication.admin import admin_required

from src import entities
from src import errors
from src import dto

app = FastAPI()
builds_storage = BuildsStorage("database/versions.json")
upload_service = UploadService(builds_storage, "database/versions")
delete_service = DeleteService(builds_storage)
version_usecase = VersionsUsecase(builds_storage)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"http://localhost:?[0-9]*$"
)

@app.post("/versions/upload_files")
async def on_upload_files(
    file: UploadFile,
    version: Annotated[str, Form()],
    description: Annotated[str, Form()]="",
    api_key: str = Depends(admin_required)
) -> entities.Build:
    build = entities.Build(version, f"database/versions/{file.filename}", description)
    
    try:
        await upload_service.add(file, build)

    except errors.BuildAlreadyExistsError as error:
        raise HTTPException(status_code=400, detail=f"{error.version} already exist")
    
    return build

@app.post("/versions/set_current_version")
async def on_set_current_version(
        version: entities.VersionSymbol,
        api_key: str = Depends(admin_required)
    ):
    try:
        version_usecase.set_current_version(version)
    
    except errors.BuildNotFoundError as error:
        raise HTTPException(status_code=400, detail=f"{error.version} not found")

@app.get('/versions/get_build_info')
async def on_get_build_info(
        version: entities.VersionSymbol,
        api_key: str = Depends(admin_required)
    ) -> entities.Build:
    try:
        return builds_storage.get_by_version(version)
    
    except errors.BuildNotFoundError as error:
        raise HTTPException(status_code=400, detail=f"{error.version} not found")

@app.delete('/versions/delete_build')
async def on_delete_build(
        version: entities.VersionSymbol,
        api_key: str = Depends(admin_required)
    ):
    delete_service.delete(version)

@app.get("/versions/get_versions")
async def on_get_current_version(api_key: str = Depends(admin_required)) -> dto.AllVersionDto:
    return dto.AllVersionDto(
        current=version_usecase.get_current_version(),
        awiable=version_usecase.get_sorted_versions()
    )

@app.get("/versions/download")
async def root() -> FileResponse:
    current = version_usecase.get_current_version()

    if current is None:
        raise HTTPException(status_code=500, detail=f"no selected version")
    
    build = builds_storage.get_by_version(current)

    return FileResponse(build.file_path, media_type="application/zip", filename="main.zip")
