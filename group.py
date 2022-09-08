from dataclasses import dataclass, field
from enum import Enum

from team import Team


class GroupName(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


@dataclass
class Group:
    name: GroupName
    teams: list[Team | None] = field(default_factory=lambda: [None, None, None, None])

    @property
    def regions(self):
        return [team.region for team in self.teams if team]

    def __str__(self):
        output = f"Group {self.name.value}:\n"
        for team in self.teams:
            output += f"{team.name};"
        return output
