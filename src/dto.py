import dataclasses
from src import entities 

@dataclasses.dataclass
class AllVersionDto:
    current: entities.VersionSymbol | None
    awiable: list[entities.VersionSymbol]
