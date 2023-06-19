import typing
import aiofiles

from src import entities
from src import versions

class CreateAbleStorage(typing.Protocol):
    def create(self, version: entities.Version): ...

class File(typing.Protocol):
    def read(self) -> typing.Coroutine[object, object, bytes]: ...
    def close(self) -> typing.Coroutine[object, object, None]: ...
    @property
    def filename(self) -> str: ...

class UploadService:
    def __init__(self, storage: CreateAbleStorage):
        self.storage = storage
        self._folder_path = "versions"
    
    async def add(self, file: File, version: versions.Version):
        file_path = f"{self._folder_path}/{file.filename}"

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        self.storage.create(entities.Version(
            version=str(version),
            file_path=file_path
        ))
