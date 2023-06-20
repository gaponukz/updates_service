from src import entities

import json
import datetime

class BuildsStorage:
    def __init__(self, filename: str):
        self._filename = filename
    
    def create(self, version: entities.Build):
        with open(self._filename, 'a') as file:
            data = {
                'version': version.version,
                'file_path': version.file_path,
                'created_at': version.created_at.isoformat(),
            }
            file.write(json.dumps(data) + '\n')
    
    def get_all(self) -> list[entities.Build]:
        all = []
        
        with open(self._filename, 'r') as file:
            for line in file:
                data = json.loads(line)
                version = entities.Build(
                    version=entities.VersionSymbol(data['version']),
                    file_path=data['file_path'],
                    created_at=datetime.datetime.fromisoformat(data['created_at']).replace(tzinfo=datetime.timezone.utc),
                )
                all.append(version)

        return all
    
    def delete_by_symbol(self, version: entities.VersionSymbol):
        lines = []
        with open(self._filename, 'r') as file:
            for line in file:
                data = json.loads(line)
                if data['version'] != version:
                    lines.append(line)
        
        with open(self._filename, 'w') as file:
            file.writelines(lines)
