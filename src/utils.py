import typing
from src import entities

class BuildProvider(typing.Protocol):
    def get_all(self) -> list[entities.Build]: ...
    def get_current_version(self) -> entities.VersionSymbol | None: ...

class BuildToVersionAdapter:
    def __init__(self, build_provider: BuildProvider):
        self._build_provider = build_provider

    def get_current_version(self) -> entities.VersionSymbol | None:
        return self._build_provider.get_current_version()
    
    def get_all_versions(self) -> list[entities.VersionSymbol]:
        builds = self._build_provider.get_all()

        return [build.version for build in builds]
