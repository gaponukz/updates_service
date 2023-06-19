from __future__ import annotations

VersionSymbol = str

class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch
    
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
            
    def is_greater_than(self, other: Version):
        if self.major > other.major:
            return True
        if self.major < other.major:
            return False
        
        if self.minor > other.minor:
            return True
        
        if self.minor < other.minor:
            return False
        
        return self.patch > other.patch
    
    def __le__(self, other: object):
        if isinstance(other, Version):
            return self.is_greater_than(other)
        
        if isinstance(other, str):
            return self == Version.from_string(other)
        
        if isinstance(other, tuple):
            return self == Version.from_tuple(
                (int(other[0]), int(other[1]), int(other[2]))
            )
        
        raise ValueError(f"Can not compare {self.__class__.__name__} with {other.__class__.__name__}")

    def __str__(self) -> VersionSymbol:
        return f"{self.major}.{self.minor}.{self.patch}"
