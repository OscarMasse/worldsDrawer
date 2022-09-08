import csv
import itertools
from copy import deepcopy, copy
from dataclasses import field, dataclass

import yaml

from group import GroupName, Group
from pool import Pool
from region import Region
from team import Team


@dataclass
class Tournament:
    groups: list[Group | None] = field(default_factory=lambda: [None, None, None, None])


def load_pools():
    pool_by_number = {
        1: Pool(number=1),
        2: Pool(number=2),
        3: Pool(number=3),
        4: Pool(number=4),
    }

    with open("teams.yaml") as file:
        raw_teams = yaml.safe_load(file)
        for raw_team in raw_teams:
            team = Team(
                name=raw_team.get("name", f"{raw_team.get('region')} seed {raw_team.get('seed')}"),
                seed=raw_team.get('seed'),
                pool=raw_team.get('pool'),
                region=Region[raw_team.get('region')],
            )
            pool_by_number[team.pool].teams.append(team)

    return pool_by_number


def create_tournaments(pool_by_number: dict[int, Pool]):
    tournaments = []

    root_tournament = Tournament(groups=[
        Group(name, [pool_by_number[1].teams[team_number]])
        for team_number, name in enumerate(GroupName)
    ])

    draw_pool(pool_by_number, 2, root_tournament, tournaments)

    return tournaments


def draw_pool(pool_by_number, pool_number, parent_tournament, tournaments):
    if pool_number == 5:
        tournaments.append(parent_tournament)
        return

    for pool in itertools.permutations(pool_by_number[pool_number].teams, 4):
        tournament = deepcopy(parent_tournament)
        fail = False
        for team, group in zip(pool, tournament.groups):
            if team.region in group.regions:
                fail = True
                break
            group.teams.append(team)

        if fail:
            continue
        draw_pool(pool_by_number, pool_number + 1, tournament, tournaments)


def main():
    pool_by_number = load_pools()

    tournaments = create_tournaments(pool_by_number)
    for index, tournament in enumerate(tournaments):
        with open(f"output/Scenario {index + 1}.csv", "w", encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Group A", "Group B", "Group C", "Group D"])
            for i in range(4):
                writer.writerow([
                    tournament.groups[0].teams[i].name,
                    tournament.groups[1].teams[i].name,
                    tournament.groups[2].teams[i].name,
                    tournament.groups[3].teams[i].name
                ])


if __name__ == '__main__':
    main()
