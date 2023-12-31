import typing
from src import entities
from src import errors

class BuildsProvider(typing.Protocol):
    def get_all(self) -> list[entities.Build]: ...
    def get_by_version(self, version: entities.VersionSymbol) -> entities.Build: ...
    def create(self, version: entities.Build): ...
    def delete_by_version(self, version: entities.VersionSymbol): ...

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
    
    def get_current_version(self) -> typing.Optional[entities.VersionSymbol]:
        current_build = [build for build in self._provider.get_all() if build.is_current]

        if not current_build:
            return None
        
        return current_build[0].version

    def set_current_version(self, version: entities.VersionSymbol):
        old = None
        new = None
        for build in self._provider.get_all():
            if not (old is None or new is None):
                break

            if build.is_current:
                build.is_current = False
                old = build
            
            if build.version == version:
                build.is_current = True
                new = build
        
        if new is None:
            raise errors.BuildNotFoundError(version)

        self._provider.delete_by_version(new.version)
        self._provider.create(new)

        if old is not None:
            self._provider.delete_by_version(old.version)
            self._provider.create(old)

    def get_all_versions(self) -> list[entities.VersionSymbol]:
        return [build.version for build in self._provider.get_all()]
