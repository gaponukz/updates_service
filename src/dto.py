import dataclasses
from src import versions 

@dataclasses.dataclass
class AllVersionDto:
    current: versions.VersionSymbol
    awiable: list[versions.VersionSymbol]
