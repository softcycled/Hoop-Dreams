from __future__ import annotations

from models import Player, Team


def make_variety_teams() -> list[Team]:

    def p(name: str, offense: int, defense: int, shooting: int, iq: int, stamina: int) -> Player:
        return Player(name, offense, defense, shooting, iq, stamina)

    return [
        # Top-tier contenders
        Team(
            "Nuggets",
            starters=[
                p("Nikola Jokic", 95, 82, 88, 96, 86),
                p("Jamal Murray", 86, 72, 86, 84, 80),
                p("Michael Porter Jr.", 80, 70, 90, 76, 78),
                p("Aaron Gordon", 78, 84, 70, 78, 86),
                p("Kentavious Caldwell-Pope", 74, 82, 84, 78, 80),
            ],
            offense_coach=88,
            defense_coach=86,
        ),
        Team(
            "Celtics",
            starters=[
                p("Jayson Tatum", 92, 82, 88, 88, 84),
                p("Jaylen Brown", 86, 78, 82, 80, 82),
                p("Kristaps Porzingis", 82, 76, 86, 78, 78),
                p("Derrick White", 80, 84, 80, 84, 82),
                p("Al Horford", 74, 80, 74, 82, 76),
            ],
            offense_coach=88,
            defense_coach=86,
        ),
        Team(
            "Mavericks",
            starters=[
                p("Luka Doncic", 94, 72, 90, 92, 82),
                p("Kyrie Irving", 88, 66, 90, 86, 80),
                p("Tim Hardaway Jr.", 78, 68, 84, 76, 78),
                p("Grant Williams", 74, 80, 74, 76, 78),
                p("Dwight Powell", 72, 76, 60, 72, 76),
            ],
            offense_coach=88,
            defense_coach=84,
        ),
        Team(
            "Bucks",
            starters=[
                p("Giannis Antetokounmpo", 93, 90, 62, 86, 90),
                p("Damian Lillard", 88, 64, 92, 86, 82),
                p("Khris Middleton", 82, 74, 86, 82, 78),
                p("Brook Lopez", 74, 88, 70, 80, 76),
                p("Malik Beasley", 74, 66, 86, 72, 78),
            ],
            offense_coach=88,
            defense_coach=86,
        ),
        Team(
            "Thunder",
            starters=[
                p("Shai Gilgeous-Alexander", 92, 88, 88, 89, 88),
                p("Chet Holmgren", 86, 84, 78, 82, 80),
                p("Jalen Williams", 82, 78, 80, 82, 80),
                p("Josh Giddey", 78, 70, 76, 84, 80),
                p("Lu Dort", 74, 88, 70, 74, 82),
            ],
            offense_coach=86,
            defense_coach=88,
        ),

        # Playoff-tier teams
        Team(
            "Lakers",
            starters=[
                p("LeBron James", 90, 82, 76, 92, 80),
                p("Anthony Davis", 85, 92, 66, 84, 78),
                p("Austin Reaves", 80, 72, 84, 82, 80),
                p("Rui Hachimura", 76, 74, 80, 74, 78),
                p("D'Angelo Russell", 82, 68, 86, 80, 76),
            ],
            offense_coach=86,
            defense_coach=84,
        ),
        Team(
            "Warriors",
            starters=[
                p("Stephen Curry", 90, 68, 96, 90, 82),
                p("Klay Thompson", 82, 72, 90, 78, 78),
                p("Andrew Wiggins", 80, 76, 78, 76, 82),
                p("Draymond Green", 74, 88, 60, 92, 84),
                p("Kevon Looney", 72, 82, 40, 78, 80),
            ],
            offense_coach=86,
            defense_coach=84,
        ),
        Team(
            "Suns",
            starters=[
                p("Kevin Durant", 92, 76, 90, 90, 82),
                p("Devin Booker", 84, 76, 88, 86, 80),
                p("Bradley Beal", 84, 70, 86, 84, 80),
                p("Jusuf Nurkic", 78, 80, 40, 78, 76),
                p("Grayson Allen", 78, 72, 86, 76, 78),
            ],
            offense_coach=86,
            defense_coach=82,
        ),
        Team(
            "76ers",
            starters=[
                p("Joel Embiid", 92, 86, 80, 88, 82),
                p("James Harden", 84, 66, 84, 90, 78),
                p("Tyrese Maxey", 82, 70, 86, 80, 82),
                p("Tobias Harris", 80, 72, 80, 78, 78),
                p("PJ Tucker", 70, 80, 60, 74, 76),
            ],
            offense_coach=86,
            defense_coach=84,
        ),
        Team(
            "Heat",
            starters=[
                p("Jimmy Butler", 88, 88, 72, 88, 82),
                p("Bam Adebayo", 84, 86, 60, 84, 84),
                p("Tyler Herro", 82, 68, 86, 78, 80),
                p("Kyle Lowry", 76, 74, 76, 82, 76),
                p("Caleb Martin", 76, 74, 78, 76, 78),
            ],
            offense_coach=84,
            defense_coach=86,
        ),
        Team(
            "Pacers",
            starters=[
                p("Tyrese Haliburton", 88, 76, 86, 92, 82),
                p("Myles Turner", 82, 86, 72, 80, 78),
                p("Buddy Hield", 82, 68, 90, 78, 78),
                p("Bennedict Mathurin", 80, 72, 82, 76, 80),
                p("Aaron Nesmith", 76, 72, 78, 74, 76),
            ],
            offense_coach=86,
            defense_coach=82,
        ),
        Team(
            "Spurs",
            starters=[
                p("Victor Wembanyama", 88, 94, 80, 86, 82),
                p("Devin Vassell", 82, 70, 84, 78, 80),
                p("Keldon Johnson", 80, 70, 80, 76, 78),
                p("Jeremy Sochan", 76, 78, 70, 76, 80),
                p("Zach Collins", 76, 78, 60, 74, 76),
            ],
            offense_coach=84,
            defense_coach=84,
        ),

        # Mid-tier teams (balanced, no 90+ offense)
        Team(
            "Kings",
            starters=[
                p("De'Aaron Fox", 84, 70, 84, 84, 84),
                p("Domantas Sabonis", 84, 80, 74, 84, 82),
                p("Kevin Huerter", 78, 70, 84, 78, 78),
                p("Harrison Barnes", 76, 72, 76, 78, 78),
                p("Keegan Murray", 78, 74, 80, 76, 80),
            ],
            offense_coach=84,
            defense_coach=82,
        ),
        Team(
            "Clippers",
            starters=[
                p("Kawhi Leonard", 84, 90, 82, 86, 80),
                p("Paul George", 82, 84, 84, 84, 80),
                p("Russell Westbrook", 76, 72, 66, 80, 78),
                p("Ivica Zubac", 76, 82, 60, 74, 76),
                p("Norman Powell", 78, 70, 82, 76, 78),
            ],
            offense_coach=84,
            defense_coach=84,
        ),
        Team(
            "Pelicans",
            starters=[
                p("Zion Williamson", 84, 78, 72, 82, 80),
                p("Brandon Ingram", 82, 72, 84, 82, 80),
                p("CJ McCollum", 80, 68, 84, 80, 78),
                p("Jonas Valanciunas", 78, 80, 70, 78, 78),
                p("Herb Jones", 74, 86, 70, 76, 80),
            ],
            offense_coach=84,
            defense_coach=84,
        ),
        Team(
            "Knicks",
            starters=[
                p("Jalen Brunson", 88, 66, 86, 86, 84),
                p("Julius Randle", 82, 72, 74, 76, 82),
                p("RJ Barrett", 78, 70, 78, 78, 80),
                p("Mitchell Robinson", 72, 88, 25, 70, 80),
                p("Quentin Grimes", 76, 74, 82, 76, 78),
            ],
            offense_coach=84,
            defense_coach=86,
        ),
        Team(
            "Grizzlies",
            starters=[
                p("Ja Morant", 84, 68, 82, 86, 82),
                p("Jaren Jackson Jr.", 82, 88, 74, 82, 80),
                p("Desmond Bane", 82, 72, 86, 82, 80),
                p("Steven Adams", 76, 84, 40, 76, 76),
                p("Dillon Brooks", 76, 78, 74, 76, 78),
            ],
            offense_coach=84,
            defense_coach=84,
        ),
        Team(
            "Magic",
            starters=[
                p("Paolo Banchero", 84, 76, 78, 82, 80),
                p("Franz Wagner", 82, 76, 82, 82, 80),
                p("Markelle Fultz", 76, 74, 72, 80, 78),
                p("Wendell Carter Jr.", 78, 82, 68, 78, 78),
                p("Cole Anthony", 76, 70, 78, 76, 78),
            ],
            offense_coach=82,
            defense_coach=84,
        ),

        # Lower-tier teams (no offense above 85)
        Team(
            "Bulls",
            starters=[
                p("Zach LaVine", 84, 68, 90, 84, 80),
                p("DeMar DeRozan", 82, 70, 80, 84, 80),
                p("Nikola Vucevic", 80, 78, 74, 82, 78),
                p("Patrick Williams", 74, 76, 70, 74, 78),
                p("Coby White", 76, 68, 80, 76, 78),
            ],
            offense_coach=82,
            defense_coach=82,
        ),
        Team(
            "Wizards",
            starters=[
                p("Kyle Kuzma", 82, 72, 78, 78, 80),
                p("Jordan Poole", 80, 64, 86, 76, 78),
                p("Deni Avdija", 76, 74, 72, 76, 78),
                p("Daniel Gafford", 74, 80, 40, 72, 76),
                p("Corey Kispert", 74, 68, 82, 74, 78),
            ],
            offense_coach=80,
            defense_coach=80,
        ),
        Team(
            "Hornets",
            starters=[
                p("LaMelo Ball", 84, 68, 88, 86, 80),
                p("Terry Rozier", 78, 66, 82, 78, 78),
                p("Gordon Hayward", 76, 72, 78, 78, 76),
                p("PJ Washington", 74, 74, 76, 74, 78),
                p("Mark Williams", 72, 78, 40, 72, 76),
            ],
            offense_coach=80,
            defense_coach=80,
        ),
        Team(
            "Nets",
            starters=[
                p("Mikal Bridges", 84, 84, 82, 84, 80),
                p("Cam Johnson", 78, 72, 86, 78, 78),
                p("Spencer Dinwiddie", 76, 68, 80, 78, 78),
                p("Nic Claxton", 72, 84, 40, 74, 78),
                p("Dorian Finney-Smith", 72, 76, 72, 74, 78),
            ],
            offense_coach=80,
            defense_coach=82,
        ),
        Team(
            "Jazz",
            starters=[
                p("Lauri Markkanen", 84, 72, 88, 82, 80),
                p("Jordan Clarkson", 80, 66, 84, 76, 78),
                p("Collin Sexton", 78, 68, 80, 76, 78),
                p("Walker Kessler", 72, 84, 40, 74, 78),
                p("Kelly Olynyk", 74, 74, 74, 76, 78),
            ],
            offense_coach=80,
            defense_coach=80,
        ),
        Team(
            "Hawks",
            starters=[
                p("Trae Young", 85, 62, 90, 88, 80),
                p("Dejounte Murray", 80, 76, 78, 82, 82),
                p("Clint Capela", 74, 84, 40, 74, 80),
                p("John Collins", 76, 70, 76, 76, 78),
                p("Bogdan Bogdanovic", 78, 66, 84, 78, 78),
            ],
            offense_coach=80,
            defense_coach=80,
        ),
    ]
