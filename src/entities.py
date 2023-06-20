import datetime
import dataclasses

VersionSymbol = str

@dataclasses.dataclass
class Build:
    version: VersionSymbol
    file_path: str
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

@dataclasses.dataclass
class Version:
    major: int
    minor: int
    patch: int
    
    @classmethod
    def from_string(cls, version: str):
        version = version.replace(" ", "").replace("\n", "").replace("\r", "")
        components = version.split(".")

        if len(components) != 3:
            raise ValueError("Invalid version format")
            
        return cls(int(components[0]), int(components[1]), int(components[2]))

    @classmethod
    def from_tuple(cls, version: tuple[int, int, int]):        
        if len(version) != 3:
            raise ValueError("Invalid version format")
            
        return cls(int(version[0]), int(version[1]), int(version[2]))

    def __str__(self) -> VersionSymbol:
        return f"{self.major}.{self.minor}.{self.patch}"
