from dataclasses import dataclass

from region import Region


@dataclass
class Team:
    name: str
    seed: int
    pool: int
    region: Region
