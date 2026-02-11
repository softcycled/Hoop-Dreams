from models import Player, Team
from sim import simulate_game


def print_box(team: Team) -> None:
    print(f"\n=== {team.name} ===")
    print("Player                  PTS  AST  REB  STL  BLK   FG     3P     FT   TOV")
    print("-" * 74)
    for p in sorted(team.starters, key=lambda p: (p.box.pts, p.box.ast, p.box.reb), reverse=True):
        fg = f"{p.box.fgm}/{p.box.fga}"
        tp = f"{p.box.tpm}/{p.box.tpa}"
        ft = f"{p.box.ftm}/{p.box.fta}"
        print(
            f"{p.name:<22} {p.box.pts:>3}  {p.box.ast:>3}  {p.box.reb:>3}  {p.box.stl:>3}  {p.box.blk:>3}  "
            f"{fg:>5}  {tp:>5}  {ft:>5}  {p.box.tov:>3}"
        )


def demo():
    home = Team(
        "Lakers",
        starters=[
            Player("LeBron James", 92, 84, 78, 92, 86),
            Player("Anthony Davis", 88, 92, 66, 84, 82),
            Player("Austin Reaves", 76, 70, 82, 80, 80),
            Player("Rui Hachimura", 74, 72, 78, 72, 80),
            Player("Jarred Vanderbilt", 66, 86, 55, 72, 84),
        ],
        offense_coach=85,
        defense_coach=85,
    )

    away = Team(
        "Warriors",
        starters=[
            Player("Stephen Curry", 90, 68, 96, 90, 82),
            Player("Klay Thompson", 78, 74, 92, 78, 78),
            Player("Andrew Wiggins", 76, 78, 78, 74, 82),
            Player("Draymond Green", 70, 92, 60, 94, 84),
            Player("Kevon Looney", 64, 82, 40, 78, 80),
        ],
        offense_coach=85,
        defense_coach=85,
    )

    res = simulate_game(home, away)
    print(f"\nFINAL: {res.home.name} {res.home_pts} - {res.away_pts} {res.away.name}")
    print_box(res.home)
    print_box(res.away)


if __name__ == "__main__":
    demo()
