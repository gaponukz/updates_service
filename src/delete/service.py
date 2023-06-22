import os
import typing
from src import entities

class DeleteAbleStorage(typing.Protocol):
    def get_by_version(self, version: entities.VersionSymbol) -> entities.Build: ...
    def delete_by_version(self, version: entities.VersionSymbol): ...

class DeleteService:
    def __init__(self, storage: DeleteAbleStorage):
        self._storage = storage
    
    def delete(self, version: entities.VersionSymbol):
        build = self._storage.get_by_version(version)
        self._storage.delete_by_version(version)

        if os.path.isfile(build.file_path):
            os.remove(build.file_path)
