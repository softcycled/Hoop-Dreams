from __future__ import annotations

from models import Player, Team


def make_variety_teams() -> list[Team]:
    """Return a small league of varied, real-player rosters.

    Goal: produce more representative batch-test behavior than filling a team
    with 5 copies of an all-time superstar.

    Notes:
    - Ratings are approximate and purely for sim tuning (0-100 scale).
    - Keep each team a mix of star + starters/role players.
    """

    def p(name: str, offense: int, defense: int, shooting: int, iq: int, stamina: int) -> Player:
        return Player(name, offense, defense, shooting, iq, stamina)

    return [
        Team(
            "Lakers",
            starters=[
                p("LeBron James", 92, 84, 78, 92, 86),
                p("Anthony Davis", 88, 92, 66, 84, 82),
                p("Austin Reaves", 76, 70, 82, 80, 80),
                p("Rui Hachimura", 74, 72, 78, 72, 80),
                p("Jarred Vanderbilt", 66, 86, 55, 72, 84),
            ],
            offense_coach=85,
            defense_coach=85,
        ),
        Team(
            "Warriors",
            starters=[
                p("Stephen Curry", 90, 68, 96, 90, 82),
                p("Klay Thompson", 78, 74, 92, 78, 78),
                p("Andrew Wiggins", 76, 78, 78, 74, 82),
                p("Draymond Green", 70, 92, 60, 94, 84),
                p("Kevon Looney", 64, 82, 40, 78, 80),
            ],
            offense_coach=85,
            defense_coach=85,
        ),
        Team(
            "Celtics",
            starters=[
                p("Jayson Tatum", 88, 80, 88, 86, 82),
                p("Jaylen Brown", 84, 78, 82, 78, 84),
                p("Jrue Holiday", 74, 88, 78, 90, 82),
                p("Derrick White", 70, 84, 80, 86, 84),
                p("Kristaps Porzingis", 80, 76, 84, 78, 78),
            ],
            offense_coach=86,
            defense_coach=86,
        ),
        Team(
            "Nuggets",
            starters=[
                p("Nikola Jokic", 92, 76, 82, 96, 80),
                p("Jamal Murray", 84, 72, 84, 82, 80),
                p("Michael Porter Jr.", 78, 70, 90, 72, 78),
                p("Aaron Gordon", 74, 82, 70, 76, 86),
                p("Kentavious Caldwell-Pope", 66, 80, 82, 78, 82),
            ],
            offense_coach=86,
            defense_coach=82,
        ),
        Team(
            "Bucks",
            starters=[
                p("Giannis Antetokounmpo", 92, 88, 62, 86, 88),
                p("Damian Lillard", 88, 64, 90, 84, 82),
                p("Khris Middleton", 78, 72, 84, 82, 78),
                p("Brook Lopez", 70, 86, 70, 78, 76),
                p("Malik Beasley", 68, 64, 86, 68, 78),
            ],
            offense_coach=86,
            defense_coach=82,
        ),
        Team(
            "Heat",
            starters=[
                p("Jimmy Butler", 86, 86, 66, 88, 80),
                p("Bam Adebayo", 78, 88, 60, 84, 86),
                p("Tyler Herro", 78, 62, 86, 74, 80),
                p("Terry Rozier", 76, 62, 82, 72, 82),
                p("Duncan Robinson", 68, 60, 92, 72, 78),
            ],
            offense_coach=84,
            defense_coach=86,
        ),
        Team(
            "Suns",
            starters=[
                p("Kevin Durant", 92, 76, 90, 88, 78),
                p("Devin Booker", 88, 66, 86, 84, 82),
                p("Bradley Beal", 82, 66, 82, 80, 78),
                p("Grayson Allen", 70, 66, 90, 74, 78),
                p("Jusuf Nurkic", 72, 78, 40, 78, 76),
            ],
            offense_coach=86,
            defense_coach=78,
        ),
        Team(
            "Knicks",
            starters=[
                p("Jalen Brunson", 86, 66, 82, 84, 84),
                p("Julius Randle", 82, 72, 74, 74, 82),
                p("OG Anunoby", 68, 90, 78, 78, 82),
                p("Mikal Bridges", 74, 86, 78, 78, 88),
                p("Mitchell Robinson", 62, 86, 25, 70, 78),
            ],
            offense_coach=84,
            defense_coach=86,
        ),
    ]
