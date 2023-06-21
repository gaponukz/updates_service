import os
import json
import datetime

from src import entities

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
        with open(self._filename, 'r') as file:
            data = json.load(file)
            builds_data = data.get('all', [])
            builds = [entities.Build(
                version=build['version'],
                file_path=build['file_path'],
                created_at=datetime.datetime.fromisoformat(build['created_at']).replace(tzinfo=datetime.timezone.utc)
            ) for build in builds_data]

            return builds
    
    def get_current_version(self) -> entities.VersionSymbol | None:
        with open(self._filename, 'r') as file:
            data = json.load(file)
            return data.get('current')

    def set_current_version(self, version: str):
        with open(self._filename, 'r+') as file:
            data = json.load(file)
            data['current'] = version
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        
    def delete_by_symbol(self, version: str):
        builds = self.get_all()
        builds = [build for build in builds if build.version != version]
        self._save_builds(builds)
    
    def _save_builds(self, builds: list[entities.Build]):
        builds_data = [
            {'version': build.version,
             'file_path': build.file_path,
             'created_at': build.created_at.isoformat()
        } for build in builds]

        with open(self._filename, 'r+') as file:
            data = json.load(file)
            data['all'] = builds_data
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def _create_new_file(self):
        content = {
            "current": None,
            "all": []
        }
        with open(self._filename, 'w') as file:
            json.dump(content, file, indent=4)
