import os
import json
import typing
import dataclasses
import datetime

from src import entities
from src import errors

class _JsonBuild(typing.TypedDict):
    version: entities.VersionSymbol
    file_path: str
    description: str
    is_current: bool
    created_at: str

class BuildsStorage:
    def __init__(self, filename: str):
        self._filename = filename

        if not os.path.exists(self._filename):
            self._create_new_file()
    
    def create(self, version: entities.Build):
        builds = self.get_all()
        builds.append(version)
        self._save_builds(builds)
    
    def get_all(self) -> list[entities.Build]:
        return self._get_all_from_file()
    
    def get_by_version(self, version: entities.VersionSymbol) -> entities.Build:
        builds = self._get_all_from_file()
        filtered = list(filter(lambda b: b.version == version, builds))
        
        if not filtered:
            raise errors.BuildNotFoundError(version)
        
        return filtered[0]
            
    def delete_by_version(self, version: entities.VersionSymbol):
        builds = self._get_all_from_file()
        self._save_builds(list(filter(lambda b: b.version != version, builds)))
    
    def _build_to_json(self, build: entities.Build) -> _JsonBuild:
        data = dataclasses.asdict(build)
        data['created_at'] = data['created_at'].isoformat()
        dumped: _JsonBuild = typing.cast(_JsonBuild, data)

        return dumped
    
    def _build_from_json(self, build: _JsonBuild) -> entities.Build:
        new_build: dict = typing.cast(dict, build.copy())
        new_build['created_at'] = datetime.datetime.fromisoformat(build['created_at'])\
            .replace(tzinfo=datetime.timezone.utc)

        return entities.Build(**new_build)
    
    def _save_builds(self, builds: list[entities.Build]):
        with open(self._filename, 'w', encoding='utf-8') as out:
            dumped_data = [self._build_to_json(build) for build in builds]
            json.dump(dumped_data, out, indent=4)
    
    def _get_all_from_file(self) -> list[entities.Build]:
        with open(self._filename, 'r', encoding='utf-8') as out:
            builds: list[_JsonBuild] = json.load(out)

            return [self._build_from_json(build) for build in builds]
        
    def _create_new_file(self) -> None:
        with open(self._filename, 'w') as file:
            json.dump([], file, indent=4)
