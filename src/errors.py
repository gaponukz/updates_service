class BuildNotFoundError(Exception):
    def __init__(self, version: str):
        self.version = version

