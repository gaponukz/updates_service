import typing
import dataclasses
from src import entities 

@dataclasses.dataclass
class AllVersionDto:
    current: typing.Optional[entities.VersionSymbol]
    awiable: list[entities.VersionSymbol]
