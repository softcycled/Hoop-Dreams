from __future__ import annotations

from typing import Dict

from sim import simulate_game
from schedule import generate_round_robin
from test_rosters import make_variety_teams


class StandingsEntry:
    def __init__(self, name: str):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.pf = 0  # points for
        self.pa = 0  # points against

    @property
    def diff(self) -> int:
        return self.pf - self.pa


def print_standings(table: Dict[str, StandingsEntry], show_pf_pa: bool = False):
    sorted_table = sorted(
        table.values(),
        key=lambda x: (x.wins, x.wins / (x.wins + x.losses if x.wins + x.losses > 0 else 1), x.diff),
        reverse=True,
    )

    print("\n=== STANDINGS ===")
    if show_pf_pa:
        print(f"{'Team':20} {'W':>3} {'L':>3} {'WIN%':>6} {'DIFF':>6} {'PF':>5} {'PA':>5}")
        print("-" * 60)
    else:
        print(f"{'Team':20} {'W':>3} {'L':>3} {'WIN%':>6} {'DIFF':>6}")
        print("-" * 40)

    for t in sorted_table:
        win_pct = t.wins / (t.wins + t.losses) if t.wins + t.losses > 0 else 0
        if show_pf_pa:
            print(f"{t.name:20} {t.wins:3} {t.losses:3} {win_pct:6.3f} {t.diff:6} {t.pf:5} {t.pa:5}")
        else:
            print(f"{t.name:20} {t.wins:3} {t.losses:3} {win_pct:6.3f} {t.diff:6}")


def play_season(
    *,
    seed: int = 1,
    teams=None,
    verbose: bool = True,
    standings_each_round: bool = True,
    show_pf_pa: bool = False,
) -> Dict[str, StandingsEntry]:
    """Simulate a full round-robin season and return final standings."""

    if teams is None:
        teams = make_variety_teams()

    team_map = {team.name: team for team in teams}
    rounds = generate_round_robin([t.name for t in teams], seed=seed)

    standings: Dict[str, StandingsEntry] = {t.name: StandingsEntry(t.name) for t in teams}

    for round_no, games in enumerate(rounds, start=1):
        if verbose:
            print(f"\n==============================")
            print(f"ROUND {round_no}")
            print(f"==============================")

        for home_name, away_name in games:
            home = team_map[home_name]
            away = team_map[away_name]

            result = simulate_game(home, away)

            standings[home_name].pf += result.home_pts
            standings[home_name].pa += result.away_pts
            standings[away_name].pf += result.away_pts
            standings[away_name].pa += result.home_pts

            if result.home_pts > result.away_pts:
                standings[home_name].wins += 1
                standings[away_name].losses += 1
            else:
                standings[away_name].wins += 1
                standings[home_name].losses += 1

            if verbose:
                print(f"{home_name} {result.home_pts} - {result.away_pts} {away_name}")

        if verbose and standings_each_round:
            print_standings(standings, show_pf_pa=show_pf_pa)

    return standings


def run_season():
    play_season(seed=1, verbose=True, standings_each_round=True, show_pf_pa=False)


if __name__ == "__main__":
    run_season()