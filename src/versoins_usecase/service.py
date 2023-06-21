import typing
from src import entities

class BuildsProvider(typing.Protocol):
    def get_all(self) -> list[entities.Build]: ...


class VersionsUsecase:
    def __init__(self, provider: BuildsProvider):
        self._provider = provider
    
    def get_sorted_versions(self, reverse:bool=False) -> list[entities.VersionSymbol]:
        versions = list(map(entities.Version.from_string, self.get_all_versions()))
        return list(map(str, sorted(versions, key=lambda v: (v.major, v.minor, v.patch), reverse=reverse)))

    def get_latest(self) -> entities.VersionSymbol:
        versions = list(map(entities.Version.from_string, self.get_all_versions()))
        latest = versions[0]

        for version in versions[1:]:
            latest = max(latest, version, key=lambda v: (v.major, v.minor, v.patch))
        
        return str(latest)
    
    def get_current_version(self) -> entities.VersionSymbol:
        current_build = [build for build in self._provider.get_all() if build.latest]

        if not current_build:
            raise ValueError("The are no current version available")
        
        return current_build[0].version

    def get_all_versions(self) -> list[entities.VersionSymbol]:
        return [build.version for build in self._provider.get_all()]
