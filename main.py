from src.application.usecase import VersionsUsecase, IVersionsUsecase
from src.infrastructure.builds_storage import BuildsStorage
from src.infrastructure.controller import app

builds_storage = BuildsStorage("database/versions.json")
version_usecase = VersionsUsecase(builds_storage, "database/versions")

app.dependency_overrides[IVersionsUsecase] = lambda: version_usecase
