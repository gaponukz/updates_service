import typing
import dataclasses
from src.domain import entities 

@dataclasses.dataclass
class AllVersionDto:
    current: typing.Optional[entities.VersionSymbol]
    awiable: list[entities.VersionSymbol]
