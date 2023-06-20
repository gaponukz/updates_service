import dataclasses
from src import entities 

@dataclasses.dataclass
class AllVersionDto:
    current: entities.VersionSymbol
    awiable: list[entities.VersionSymbol]
