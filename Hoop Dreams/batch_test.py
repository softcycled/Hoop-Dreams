from __future__ import annotations

import argparse
import random
import statistics
from dataclasses import dataclass

from sim import simulate_game
from test_rosters import make_variety_teams


@dataclass
class BatchSummary:
    games: int
    teams: int
    avg_team_pts: float
    avg_total_pts: float
    avg_team_fta: float
    min_team_pts: int
    max_team_pts: int
    teams_ge_120: int
    teams_ge_130: int
    teams_ge_140: int
    star_fta_avgs: dict[str, float]


def _pick_matchup(rng: random.Random, teams: list) -> tuple:
    i = rng.randrange(len(teams))
    j = rng.randrange(len(teams) - 1)
    if j >= i:
        j += 1
    return teams[i], teams[j]


def run_batch(games: int, seed: int | None) -> BatchSummary:
    rng = random.Random(seed)
    teams = make_variety_teams()

    # Define "stars" for reporting using roster ratings (no extra traits needed).
    stars = {
        p.name
        for team in teams
        for p in team.starters
        if p.offense >= 88
    }
    star_totals: dict[str, int] = {name: 0 for name in stars}
    star_games: dict[str, int] = {name: 0 for name in stars}

    team_points: list[int] = []
    team_ftas: list[int] = []
    for _ in range(games):
        home, away = _pick_matchup(rng, teams)
        result = simulate_game(home, away)
        team_points.append(result.home_pts)
        team_points.append(result.away_pts)

        home_fta = sum(p.box.fta for p in result.home.starters)
        away_fta = sum(p.box.fta for p in result.away.starters)
        team_ftas.append(home_fta)
        team_ftas.append(away_fta)

        for team in (result.home, result.away):
            for p in team.starters:
                if p.name in star_totals:
                    star_totals[p.name] += p.box.fta
                    star_games[p.name] += 1

    avg_team_pts = statistics.fmean(team_points) if team_points else 0.0
    avg_team_fta = statistics.fmean(team_ftas) if team_ftas else 0.0
    star_fta_avgs = {
        name: (star_totals[name] / star_games[name]) if star_games[name] else 0.0
        for name in sorted(stars)
    }
    return BatchSummary(
        games=games,
        teams=len(teams),
        avg_team_pts=avg_team_pts,
        avg_total_pts=2.0 * avg_team_pts,
        avg_team_fta=avg_team_fta,
        min_team_pts=min(team_points) if team_points else 0,
        max_team_pts=max(team_points) if team_points else 0,
        teams_ge_120=sum(1 for p in team_points if p >= 120),
        teams_ge_130=sum(1 for p in team_points if p >= 130),
        teams_ge_140=sum(1 for p in team_points if p >= 140),
        star_fta_avgs=star_fta_avgs,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch-run random matchups for trend testing")
    parser.add_argument("--games", type=int, default=200, help="number of games to simulate")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    args = parser.parse_args()

    summary = run_batch(games=args.games, seed=args.seed)
    team_games = summary.games * 2

    print(
        "teams",
        summary.teams,
        "games",
        summary.games,
        "team_games",
        team_games,
        "avg_team_pts",
        f"{summary.avg_team_pts:.1f}",
        "avg_total_pts",
        f"{summary.avg_total_pts:.1f}",
        "avg_team_fta",
        f"{summary.avg_team_fta:.2f}",
        "min_team_pts",
        summary.min_team_pts,
        "max_team_pts",
        summary.max_team_pts,
        "teams_120plus",
        summary.teams_ge_120,
        "teams_130plus",
        summary.teams_ge_130,
        "teams_140plus",
        summary.teams_ge_140,
    )

    print("star_fta_averages")
    for name, avg_fta in summary.star_fta_avgs.items():
        print(name, f"{avg_fta:.2f}")


if __name__ == "__main__":
    main()
