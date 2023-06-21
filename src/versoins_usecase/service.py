import typing
from src import entities

class VersionsProvider(typing.Protocol):
    def get_current_version(self) -> entities.VersionSymbol | None: ...
    def get_all_versions(self) -> list[entities.VersionSymbol]: ...


class VersionsUsecase:
    def __init__(self, provider: VersionsProvider):
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
        version = self._provider.get_current_version()

        if version is None:
            raise ValueError("Provided current version is not available")
        
        return version

    def get_all_versions(self) -> list[entities.VersionSymbol]:
        return self._provider.get_all_versions()
    
