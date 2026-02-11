from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Matchup:
    round_no: int
    home: str
    away: str


def generate_round_robin(team_names: List[str], seed: int | None = None) -> List[List[Tuple[str, str]]]:
    """
    Generate a single round-robin schedule (everyone plays everyone once).
    Returns a list of rounds, where each round is a list of (home, away) pairs.

    Uses the classic "circle method".
    Requirements:
      - len(team_names) must be even
      - team_names must be unique
    """
    n = len(team_names)
    if n < 2:
        raise ValueError("Need at least 2 teams")
    if n % 2 != 0:
        raise ValueError("Number of teams must be even for this generator")
    if len(set(team_names)) != n:
        raise ValueError("Team names must be unique")

    teams = team_names[:]

    # Optional deterministic shuffle via seed (simple LCG-ish shuffle to avoid importing random everywhere)
    # If you don't care, just pass seed=None and keep team order stable.
    if seed is not None:
        # Fisher–Yates with a tiny deterministic PRNG
        x = seed & 0xFFFFFFFF

        def rnd():
            nonlocal x
            x = (1664525 * x + 1013904223) & 0xFFFFFFFF
            return x

        for i in range(n - 1, 0, -1):
            j = rnd() % (i + 1)
            teams[i], teams[j] = teams[j], teams[i]

    rounds: List[List[Tuple[str, str]]] = []
    fixed = teams[-1]
    rotating = teams[:-1]  # length n-1

    # total rounds = n - 1
    for r in range(n - 1):
        left = rotating[: (n // 2) - 1]
        right = rotating[(n // 2) - 1 :][::-1]

        pairings: List[Tuple[str, str]] = []

        # Pair fixed team with first of right side
        # Alternate home/away by round to spread home games
        if r % 2 == 0:
            pairings.append((fixed, right[0]))
        else:
            pairings.append((right[0], fixed))

        # Pair remaining teams
        for i in range(len(left)):
            a = left[i]
            b = right[i + 1]
            if r % 2 == 0:
                pairings.append((a, b))
            else:
                pairings.append((b, a))

        rounds.append(pairings)

        # Rotate: move last of rotating to front (classic circle)
        rotating = [rotating[-1]] + rotating[:-1]

    return rounds


def flatten_rounds(rounds: List[List[Tuple[str, str]]]) -> List[Matchup]:
    """Convert rounds structure into a flat list of Matchup objects."""
    out: List[Matchup] = []
    for i, games in enumerate(rounds, start=1):
        for home, away in games:
            out.append(Matchup(round_no=i, home=home, away=away))
    return out


def validate_round_robin(team_names: List[str], rounds: List[List[Tuple[str, str]]]) -> None:
    """Raise ValueError if schedule is invalid."""
    n = len(team_names)
    expected_rounds = n - 1
    if len(rounds) != expected_rounds:
        raise ValueError(f"Expected {expected_rounds} rounds, got {len(rounds)}")

    # Each round: every team appears exactly once
    for idx, games in enumerate(rounds, start=1):
        seen = set()
        for h, a in games:
            if h == a:
                raise ValueError(f"Round {idx}: team plays itself ({h})")
            if h in seen or a in seen:
                raise ValueError(f"Round {idx}: a team appears twice")
            seen.add(h)
            seen.add(a)
        if seen != set(team_names):
            missing = set(team_names) - seen
            extra = seen - set(team_names)
            raise ValueError(f"Round {idx}: missing={missing}, extra={extra}")

    # Global: every unordered pair appears exactly once
    pairs = set()
    for games in rounds:
        for h, a in games:
            key = tuple(sorted((h, a)))
            if key in pairs:
                raise ValueError(f"Duplicate matchup detected: {key}")
            pairs.add(key)

    expected_pairs = n * (n - 1) // 2
    if len(pairs) != expected_pairs:
        raise ValueError(f"Expected {expected_pairs} unique matchups, got {len(pairs)}")


# Quick manual test
if __name__ == "__main__":
    teams = [
    "Lakers", "Warriors", "Nuggets", "Suns",
    "Mavericks", "Clippers", "Kings", "Pelicans",
    "Timberwolves", "Thunder", "Grizzlies", "Rockets",
    "Celtics", "Bucks", "Heat", "Knicks",
    "76ers", "Cavaliers", "Hawks", "Bulls",
    "Pacers", "Magic", "Raptors", "Nets",
]
    rounds = generate_round_robin(teams, seed=1)
    validate_round_robin(teams, rounds)

    print(f"Rounds: {len(rounds)}")
    print(f"Games per round: {len(rounds[0])}")
    print("Round 1 sample:")
    for h, a in rounds[0]:
        print(f"  {h} vs {a}")