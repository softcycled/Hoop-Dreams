from __future__ import annotations

import argparse
import random
from typing import Dict, Iterable, List, Tuple

from season import StandingsEntry, play_season
from test_rosters import make_variety_teams


def _sort_key(e: StandingsEntry) -> tuple:
    games = e.wins + e.losses
    win_pct = e.wins / games if games else 0.0
    return (e.wins, win_pct, e.diff)


def _ranked(standings: Dict[str, StandingsEntry]) -> List[StandingsEntry]:
    return sorted(standings.values(), key=_sort_key, reverse=True)


def run_balance_check(n_seasons: int = 50, seed: int = 1) -> None:
    # Reproducible randomness across runs, while still allowing seasons to vary.
    random.seed(seed)

    teams = make_variety_teams()
    team_names = [t.name for t in teams]

    wins_by_team: Dict[str, List[int]] = {name: [] for name in team_names}
    diff_by_team: Dict[str, List[int]] = {name: [] for name in team_names}

    seasons_with_20_wins = 0
    seasons_130plus = 0
    seasons_140plus = 0
    best_wins: List[int] = []
    worst_wins: List[int] = []
    best_diff: List[int] = []
    worst_diff: List[int] = []

    for _ in range(n_seasons):
        standings = play_season(seed=1, teams=teams, verbose=False)
        ranked = _ranked(standings)

        if max(e.wins for e in ranked) >= 20:
            seasons_with_20_wins += 1

        best = ranked[0]
        worst = ranked[-1]
        best_wins.append(best.wins)
        worst_wins.append(worst.wins)
        best_diff.append(best.diff)
        worst_diff.append(worst.diff)
        
        if best.diff >= 130:
            seasons_130plus += 1
        if best.diff >= 140:
            seasons_140plus += 1

        for e in ranked:
            wins_by_team[e.name].append(e.wins)
            diff_by_team[e.name].append(e.diff)

    top5 = sorted(
        team_names,
        key=lambda name: (sum(wins_by_team[name]) / n_seasons, sum(diff_by_team[name]) / n_seasons),
        reverse=True,
    )[:5]

    def avg(nums: Iterable[int]) -> float:
        nums = list(nums)
        return sum(nums) / len(nums) if nums else 0.0

    print(f"Balance check over {n_seasons} seasons (schedule seed=1, rng seed={seed})")
    print(f"Any team >= 20 wins: {seasons_with_20_wins}/{n_seasons} ({seasons_with_20_wins / n_seasons:.1%})")
    print(f"Avg wins: #1 team = {avg(best_wins):.2f}, #24 team = {avg(worst_wins):.2f}")
    print(f"Avg DIFF: #1 team = {avg(best_diff):.1f}, #24 team = {avg(worst_diff):.1f}")
    print(f"Teams with DIFF >= 130: {seasons_130plus}/{n_seasons} seasons")
    print(f"Teams with DIFF >= 140: {seasons_140plus}/{n_seasons} seasons")

    print("Top 5 teams by average wins:")
    for i, name in enumerate(top5, start=1):
        print(
            f"  {i}. {name}: {avg(wins_by_team[name]):.2f} wins, {avg(diff_by_team[name]):.1f} DIFF"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--seasons", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1, help="RNG seed (schedule seed is fixed to 1)")
    args = parser.parse_args()

    run_balance_check(n_seasons=args.seasons, seed=args.seed)


if __name__ == "__main__":
    main()
