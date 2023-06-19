import datetime
import dataclasses
from src import versions

@dataclasses.dataclass
class Build:
    version: versions.VersionSymbol
    file_path: str
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
