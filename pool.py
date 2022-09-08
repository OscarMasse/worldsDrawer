from dataclasses import dataclass, field

from team import Team


@dataclass
class Pool:
    number: int
    teams: list[Team] = field(default_factory=list[Team])
