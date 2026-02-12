from __future__ import annotations

from models import Team, Player
from sim import simulate_game
from test_rosters import make_variety_teams


def _fmt_box_line(p: Player) -> str:
    b = p.box
    fg = f"{b.fgm}-{b.fga}"
    tp = f"{b.tpm}-{b.tpa}"
    ft = f"{b.ftm}-{b.fta}"
    return (
        f"{p.name:<18} "
        f"PTS {b.pts:>3}  REB {b.reb:>2}  AST {b.ast:>2}  "
        f"STL {b.stl:>2}  BLK {b.blk:>2}  TOV {b.tov:>2}  "
        f"FG {fg:>7}  3P {tp:>7}  FT {ft:>7}  PF {b.pf:>2}"
    )


def _print_team_box_score(team: Team, team_pts: int, highlight_threshold: int) -> None:
    print(f"{team.name} — {team_pts}")
    for p in team.starters:
        prefix = ">> " if p.box.pts >= highlight_threshold else "   "
        print(prefix + _fmt_box_line(p))


def run_superstar_test(
    num_games: int = 200,
    boxscore_examples: int = 1,
    threshold: int = 50,
    ensure_example: bool = True,
    max_extra_games: int = 3000,
) -> None:
    """Run games and report superstar scoring distribution.

    If any starter hits `threshold`+ points, prints up to `boxscore_examples`
    example box scores.
    """
    teams = make_variety_teams()
    
    counts_30plus = 0
    counts_40plus = 0
    counts_45plus = 0
    counts_50plus = 0
    counts_55plus = 0
    counts_60plus = 0
    max_pts = 0
    team_140plus = 0
    total_games = 0
    examples_printed = 0

    def maybe_print_example(result) -> None:
        nonlocal examples_printed
        if examples_printed >= boxscore_examples:
            return

        top_scorer = max((p.box.pts for p in result.home.starters + result.away.starters), default=0)
        if top_scorer < threshold:
            return

        meta = getattr(result, "meta", "")
        meta = f" {meta}" if meta else ""
        print("\n" + "=" * 72)
        print(
            f"BOX SCORE EXAMPLE ({threshold}+ game) — Final: "
            f"{result.home.name} {result.home_pts}, {result.away.name} {result.away_pts}{meta}"
        )
        print(f"(Players with {threshold}+ are prefixed with '>>')")
        print("-" * 72)
        _print_team_box_score(result.home, result.home_pts, threshold)
        print("-" * 72)
        _print_team_box_score(result.away, result.away_pts, threshold)
        print("=" * 72 + "\n")
        examples_printed += 1

    for i in range(num_games):
        home = teams[i % len(teams)]
        away = teams[(i + 1) % len(teams)]

        result = simulate_game(home, away)

        maybe_print_example(result)
        
        # Check each team's players for 30+, 40+, 45+, 50+ performances
        home_max = max(p.box.pts for p in home.starters)
        away_max = max(p.box.pts for p in away.starters)

        # Assert: any 50+ scorer must be a true superstar (offense >= 90)
        for p in home.starters + away.starters:
            if p.box.pts >= 50:
                assert (
                    p.offense >= 90
                ), f"Found {p.box.pts} points by non-superstar (offense={p.offense}) — {p.name}"
        
        if home_max >= 30:
            counts_30plus += 1
        if home_max >= 40:
            counts_40plus += 1
        if home_max >= 45:
            counts_45plus += 1
        if home_max >= 50:
            counts_50plus += 1
        if home_max >= 55:
            counts_55plus += 1
        if home_max >= 60:
            counts_60plus += 1
        max_pts = max(max_pts, home_max)
        
        if away_max >= 30:
            counts_30plus += 1
        if away_max >= 40:
            counts_40plus += 1
        if away_max >= 45:
            counts_45plus += 1
        if away_max >= 50:
            counts_50plus += 1
        if away_max >= 55:
            counts_55plus += 1
        if away_max >= 60:
            counts_60plus += 1
        max_pts = max(max_pts, away_max)
        
        if result.home_pts >= 140:
            team_140plus += 1
        if result.away_pts >= 140:
            team_140plus += 1
        
        total_games += 2

    print(f"Superstar Test Results ({num_games} games, {total_games} team games)")
    print(f"Games with 30+ points: {counts_30plus} ({counts_30plus / total_games:.1%})")
    print(f"Games with 40+ points: {counts_40plus} ({counts_40plus / total_games:.1%})")
    print(f"Games with 45+ points: {counts_45plus} ({counts_45plus / total_games:.1%})")
    print(f"Games with 50+ points: {counts_50plus} ({counts_50plus / total_games:.1%})")
    print(f"Games with 55+ points: {counts_55plus} ({counts_55plus / total_games:.1%})")
    print(f"Games with 60+ points: {counts_60plus} ({counts_60plus / total_games:.1%})")
    print(f"Max individual points in a game: {max_pts}")
    print(f"Team games with 140+ points: {team_140plus}/{total_games} ({team_140plus / total_games:.1%})")

    if boxscore_examples > 0 and examples_printed == 0:
        print(f"\nNo {threshold}+ point game occurred in the first {num_games} games.")

    if ensure_example and boxscore_examples > 0 and examples_printed < boxscore_examples:
        extra_games = 0
        i = num_games
        while examples_printed < boxscore_examples and extra_games < max_extra_games:
            home = teams[i % len(teams)]
            away = teams[(i + 1) % len(teams)]
            result = simulate_game(home, away)
            maybe_print_example(result)
            extra_games += 1
            i += 1

        if examples_printed < boxscore_examples:
            print(
                f"Still no {threshold}+ example after {num_games + extra_games} total games. "
                f"Try lowering `threshold` or increasing `max_extra_games`."
            )


if __name__ == "__main__":
    run_superstar_test(num_games=200, boxscore_examples=1, threshold=50, ensure_example=True, max_extra_games=3000)
