from dataclasses import dataclass, field
from typing import List


@dataclass
class BoxLine:
    pts: int = 0
    reb: int = 0
    ast: int = 0
    stl: int = 0
    blk: int = 0
    tov: int = 0
    fga: int = 0
    fgm: int = 0
    tpa: int = 0
    tpm: int = 0
    fta: int = 0
    ftm: int = 0
    pf: int = 0


@dataclass
class Player:
    name: str
    offense: int   # 1-99
    defense: int   # 1-99
    shooting: int  # 1-99
    iq: int        # 1-99
    stamina: int   # 1-99
    box: BoxLine = field(default_factory=BoxLine)


@dataclass
class Team:
    name: str
    starters: List[Player]
    offense_coach: int = 70
    defense_coach: int = 70


@dataclass
class GameResult:
    home: Team
    away: Team
    home_pts: int
    away_pts: int
    possessions: int
