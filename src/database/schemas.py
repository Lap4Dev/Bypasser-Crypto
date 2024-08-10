import dataclasses


@dataclasses.dataclass
class DatabaseConfig:
    url: str
    echo: bool = False


