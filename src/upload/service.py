import typing
import aiofiles

from src import entities

class CreateAbleStorage(typing.Protocol):
    def create(self, build: entities.Build): ...

class File(typing.Protocol):
    def read(self) -> typing.Coroutine[object, object, bytes]: ...
    def close(self) -> typing.Coroutine[object, object, None]: ...
    @property
    def filename(self) -> typing.Optional[str]: ...

class UploadService:
    def __init__(self, storage: CreateAbleStorage, folder_path):
        self.storage = storage
        self._folder_path = folder_path
    
    async def add(self, file: File, version: entities.Version):
        file_path = f"{self._folder_path}/{file.filename}"

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        self.storage.create(entities.Build(
            version=str(version),
            file_path=file_path
        ))
