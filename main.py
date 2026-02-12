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
        "Thunder",
        starters=[
            Player("SGA", 93, 87, 88, 90, 88),
            Player("Josh Giddey", 80, 70, 78, 86, 80),
            Player("Jalen Williams", 78, 76, 80, 82, 78),
            Player("Chet Holmgren", 84, 82, 76, 80, 78),
            Player("Lu Dort", 68, 88, 70, 74, 80),
        ],
        offense_coach=84,
        defense_coach=86,
    )

    away = Team(
        "Nuggets",
        starters=[
            Player("Nikola Jokic", 95, 82, 88, 96, 86),
            Player("Jamal Murray", 86, 74, 86, 84, 80),
            Player("Michael Porter Jr.", 80, 72, 92, 74, 78),
            Player("Aaron Gordon", 76, 84, 72, 78, 86),
            Player("KCP", 70, 82, 84, 78, 80),
        ],
        offense_coach=86,
        defense_coach=84,
    )

    res = simulate_game(home, away)
    print(f"\nFINAL: {res.home.name} {res.home_pts} - {res.away_pts} {res.away.name}")
    print_box(res.home)
    print_box(res.away)


if __name__ == "__main__":
    demo()
