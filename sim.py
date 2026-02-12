import random
from models import Team, GameResult


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def ft_make_prob(player) -> float:
    # Rough FT% proxy from shooting + IQ; clamped to sane bounds.
    rating = player.shooting * 0.65 + player.iq * 0.35
    return clamp(0.67 + (rating - 50) / 220.0, 0.58, 0.93)


def reset_box(team: Team) -> None:
    for p in team.starters:
        p.box = type(p.box)()


def team_avg(team: Team):
    off = sum(p.offense for p in team.starters) / 5
    de = sum(p.defense for p in team.starters) / 5
    sh = sum(p.shooting for p in team.starters) / 5
    iq = sum(p.iq for p in team.starters) / 5
    st = sum(p.stamina for p in team.starters) / 5
    return off, de, sh, iq, st

# Flatter volume distribution so stars don't take an extreme share.
ROLE_TARGETS = [0.30, 0.24, 0.18, 0.15, 0.13]  # sums to 1.00


def role_targets_for_team(team: Team):
    """
    Returns dict[starter_index] -> target_share (rough FGA share).
    Determined by ranking starters by offense.
    """
    ranked = sorted(enumerate(team.starters), key=lambda t: t[1].offense, reverse=True)
    targets: dict[int, float] = {}
    for rank, (starter_index, _) in enumerate(ranked):
        targets[starter_index] = ROLE_TARGETS[rank]
    return targets


def choose_shooter(team: Team, quarter: int = 0):
    """
    Shooter selection = (player ability) * (role target share) with:
    - soft cap if a player exceeds their target share
    - cold-night correction: shift even more to PRIMARY when bricking
    - superstar redistribution: boost hot star with O>=90, FGA>=20, FG%>=0.52 in Q3+
    """
    total_fga = sum(p.box.fga for p in team.starters) + 1
    total_fgm = sum(p.box.fgm for p in team.starters)
    team_fg = total_fgm / max(1, total_fga)

    targets = role_targets_for_team(team)

    # identify primary (highest offense)
    primary = max(team.starters, key=lambda p: p.offense)

    # Takeover logic (Q3+ only): once a TRUE superstar gets hot, we allow
    # them to temporarily exceed normal usage limits.
    # IMPORTANT: takeover eligibility is STRICTLY gated by offense >= 90.
    takeover_player = getattr(team, "_takeover_player", None)
    if quarter >= 3 and takeover_player is None and not getattr(team, "_takeover_triggered", False):
        # Find the best eligible candidate (highest offense first)
        for p in sorted(team.starters, key=lambda pl: pl.offense, reverse=True):
            if p.offense < 90:
                continue
            if p.box.fga < 20:
                continue
            fg_pct = p.box.fgm / p.box.fga if p.box.fga > 0 else 0.0
            if fg_pct >= 0.52:
                takeover_player = p
                team._takeover_player = p
                team._takeover_triggered = True
                break

    weights = []
    for starter_index, p in enumerate(team.starters):
        # ability weight (kept close to your original)
        ability = p.offense * 0.72 + p.shooting * 0.82 + p.iq * 0.18

        # role share drives volume
        target = targets[starter_index]

        # how much he's already taking
        current_share = p.box.fga / total_fga

        # Takeover effect: boost ONLY the takeover player and ONLY in Q3+.
        # This increases shot volume by raising the usage target cap and
        # slightly suppressing teammates (volume redistribution) without
        # affecting make%.
        if quarter >= 3 and takeover_player is not None:
            if p is takeover_player:
                target = min(0.55, target + 0.22)
            else:
                ability *= 0.85

        # Non-superstars should essentially never reach true takeover volumes.
        # This is a volume guardrail (no make% changes) to keep 50+ games
        # restricted to offense >= 90 players in practice.
        if p.offense < 90 and current_share > 0.38:
            ability *= 0.12

        # soft cap: if already above target, dampen strongly
        # (lets stars be stars, but forces "one ball" realism)
        if current_share > target:
            ability *= 0.30

        # glue/low-role leash: prevents random chucking
        # if you are a low-role guy and already above your lane, cut you off hard
        if target <= 0.10 and current_share > (target + 0.04):
            ability *= 0.25

        # cold-night correction: if team is bricking, lean more on the primary
        if team_fg < 0.38 and p is primary:
            ability *= 1.18

        # final weight is ability scaled by role target (volume intent)
        w = max(0.01, ability * (0.70 + target))  # target boosts, but doesn't dominate
        weights.append(w)

    return random.choices(team.starters, weights=weights, k=1)[0]


def simulate_bench_possession(off: Team, deff: Team, quarter: int, clutch: bool) -> int:
    """Simulate a possession that belongs to bench / dead minutes.

    We still want those possessions to produce points (to avoid 70-80 point games),
    but we don't attribute stats to starters.
    """

    off_off, _, off_sh, off_iq, off_st = team_avg(off)
    _, def_def, _, _, _ = team_avg(deff)

    # Bench units are typically worse than starters.
    off_off -= 5
    off_sh -= 5
    off_iq -= 3
    off_st -= 3

    fatigue = (quarter - 1) * 0.09
    fatigue_pen = fatigue * (100 - off_st) / 100.0

    tov = (
        0.115
        + (50 - off_iq) / 420.0
        + (def_def - 50) / 520.0
        + fatigue_pen * 0.25
        + (0.02 if clutch else 0.0)
    )
    tov = clamp(tov, 0.07, 0.30)
    if random.random() < tov:
        return 0

    three_rate = (
        0.26
        + (off_sh - 50) / 300.0
        + (off.offense_coach - 50) / 420.0
        + (0.02 if clutch else 0.0)
    )
    three_rate = clamp(three_rate, 0.16, 0.38)

    if random.random() < three_rate:
        make3 = (
            0.30
            + (off_sh - 50) / 240.0
            + (off.offense_coach - 50) / 520.0
            - (def_def - 50) / 330.0
            - (deff.defense_coach - 50) / 520.0
            - fatigue_pen * 0.26
        )
        make3 = clamp(make3, 0.17, 0.48)
        return 3 if random.random() < make3 else 0

    make2 = (
        0.45
        + (off_off - 50) / 240.0
        + (off.offense_coach - 50) / 620.0
        - (def_def - 50) / 310.0
        - fatigue_pen * 0.22
        - (0.01 if clutch else 0.0)
    )
    make2 = clamp(make2, 0.23, 0.72)
    return 2 if random.random() < make2 else 0


def simulate_possession(off: Team, deff: Team, quarter: int, clutch: bool) -> int:
    off_off, off_def, off_sh, off_iq, off_st = team_avg(off)
    def_off, def_def, def_sh, def_iq, def_st = team_avg(deff)

    # Fatigue since starters are effectively playing "all game"
    fatigue = (quarter - 1) * 0.09
    fatigue_pen = fatigue * (100 - off_st) / 100.0

    # turnovers (same core idea)
    tov = (
        0.11
        + (50 - off_iq) / 620.0
        + (def_def - 50) / 820.0
        + fatigue_pen * 0.30
        + (0.03 if clutch else 0.0)
    )
    tov = clamp(tov, 0.06, 0.28)

    if random.random() < tov:
        handler = random.choices(
            off.starters,
            weights=[p.offense * 0.7 + p.iq * 0.9 for p in off.starters],
            k=1,
        )[0]
        handler.box.tov += 1

        # Some turnovers are forced (steals).
        forced = clamp(0.30 + (def_def - 50) / 140.0 - (off_iq - 50) / 220.0, 0.12, 0.58)
        if random.random() < forced:
            thief = random.choices(
                deff.starters,
                weights=[p.defense * 0.75 + p.iq * 0.25 for p in deff.starters],
                k=1,
            )[0]
            thief.box.stl += 1
        return 0

    # Pick shooter FIRST (so shooter can influence 3pt tendency realistically)
    shooter = choose_shooter(off, quarter=quarter)

    # Mild hot-shooting regression to reduce extreme outliers.
    # - If team FG% > 0.54 after 16+ FGA: -0.02 to future 2PT & 3PT make%
    # - If team 3P% > 0.45 after 9+ 3PA: additional -0.02 to future 3PT make%
    # - Cap total penalty at 0.04.
    team_fga = sum(p.box.fga for p in off.starters)
    team_fgm = sum(p.box.fgm for p in off.starters)
    team_tpa = sum(p.box.tpa for p in off.starters)
    team_tpm = sum(p.box.tpm for p in off.starters)

    reg_2pt = 0.0
    reg_3pt = 0.0
    if team_fga >= 16 and (team_fgm / max(1, team_fga)) > 0.54:
        reg_2pt += 0.02
        reg_3pt += 0.02
    if team_tpa >= 9 and (team_tpm / max(1, team_tpa)) > 0.45:
        reg_3pt += 0.02

    reg_2pt = clamp(reg_2pt, 0.0, 0.04)
    reg_3pt = clamp(reg_3pt, 0.0, 0.04)

    # 3pt tendency (team-level baseline)
    three_rate = (
        0.27
        + (off_sh - 50) / 270.0
        + (off.offense_coach - 50) / 330.0
        + (0.03 if clutch else 0.0)
    )

    # Fix from your code: this must happen BEFORE take_three is decided
    # (you previously changed three_rate after take_three was already chosen)
    if shooter.offense >= 90 and shooter.shooting < 85:
        three_rate -= 0.04  # superstar who isn't a sniper: fewer 3s

    three_rate = clamp(three_rate, 0.18, 0.38)
    take_three = random.random() < three_rate

    # Star shot quality boost (same idea as your code)
    shot_quality = 0.0
    if shooter.offense >= 90:
        shot_quality += 0.03
    if shooter.iq >= 85:
        shot_quality += 0.01

    # Defensive attention for elite shooters + clutch pressure
    attention = 0.0
    if shooter.shooting >= 90:
        attention += 0.03
    if clutch:
        attention += 0.01

    if take_three:
        shooter.box.tpa += 1
        shooter.box.fga += 1

        make = (
            0.31
            + (shooter.shooting - 50) / 370.0
            + (off.offense_coach - 50) / 630.0
            - (def_def - 50) / 490.0
            - (deff.defense_coach - 50) / 680.0
            - fatigue_pen * 0.30
            - attention
            + shot_quality
        )
        make -= reg_3pt
        
        # Soft parity dampener: reduce make% stretch based on team skill gap
        team_gap = off_off - def_def
        parity_factor = 1.0 - (team_gap / 450.0)
        make *= clamp(parity_factor, 0.82, 1.10)
        
        make = clamp(make, 0.19, 0.49)

        made = random.random() < make

        # Fouls on jumpers are rarer but exist (and-1 / 3 FTs).
        foul_chance = (
            0.022
            + (shooter.offense - 50) / 1800.0
            + (off.offense_coach - 50) / 2200.0
            - (def_def - 50) / 2400.0
            + (0.010 if clutch else 0.0)
        )
        # Foul tuning: keep global at 0.95, but shift fouls toward 2PT and away from 3PT.
        foul_mult_global = 0.95
        foul_mult_3pt = 0.55
        foul_chance *= foul_mult_global * foul_mult_3pt

        # Smaller star bias on 3s (most FTs should come from drives/paint pressure).
        foul_bias = 1.0 + (shooter.offense - 80) / 520.0
        foul_bias = clamp(foul_bias, 0.94, 1.08)
        foul_chance *= foul_bias
        foul_chance = clamp(foul_chance, 0.008, 0.06)
        fouled = random.random() < foul_chance

        if made:
            points = 3
            shooter.box.tpm += 1
            shooter.box.fgm += 1
            shooter.box.pts += 3

            # and-1 FT
            if fouled:
                shooter.box.fta += 1
                if random.random() < ft_make_prob(shooter):
                    shooter.box.ftm += 1
                    shooter.box.pts += 1
                    points += 1

                fouler = random.choices(deff.starters, weights=[p.defense for p in deff.starters], k=1)[0]
                fouler.box.pf += 1

            # assists (slightly increased so the offense doesn't look like pure iso)
            if random.random() < clamp(0.44 + (off_iq - 50) / 150.0, 0.24, 0.74):
                passers = [p for p in off.starters if p is not shooter]
                passer = random.choices(passers, weights=[p.iq for p in passers], k=1)[0]
                passer.box.ast += 1
            return points
        else:
            # Shooting foul -> 3 free throws on miss
            if fouled:
                fouler = random.choices(deff.starters, weights=[p.defense for p in deff.starters], k=1)[0]
                fouler.box.pf += 1

                shooter.box.fta += 3
                ft_prob = ft_make_prob(shooter)
                made_fts = 0
                for _ in range(3):
                    if random.random() < ft_prob:
                        shooter.box.ftm += 1
                        shooter.box.pts += 1
                        made_fts += 1
                return made_fts

            rebounder = random.choices(
                off.starters + deff.starters,
                weights=[p.defense + p.stamina for p in off.starters + deff.starters],
                k=1,
            )[0]
            rebounder.box.reb += 1
            return 0

    # 2pt attempt
    shooter.box.fga += 1

    # 2PT shot-type split: rim vs midrange.
    rim_rate = clamp(
        0.45 + (shooter.offense - 75) / 200.0 - (shooter.shooting - 75) / 250.0,
        0.30,
        0.70,
    )
    is_rim = random.random() < rim_rate

    make = (
        0.46
        + (shooter.offense - 50) / 340.0
        + (off.offense_coach - 50) / 820.0
        - (def_def - 50) / 470.0
        - fatigue_pen * 0.24
        - (0.01 if clutch else 0.0)
        + shot_quality
    )

    make -= reg_2pt

    # Rim attempts are a bit higher %; midrange a bit lower %.
    make += 0.04 if is_rim else -0.03
    
    # Soft parity dampener: reduce make% stretch based on team skill gap
    team_gap = off_off - def_def
    parity_factor = 1.0 - (team_gap / 450.0)
    make *= clamp(parity_factor, 0.82, 1.10)
    
    make = clamp(make, 0.24, 0.73)

    made = random.random() < make

    # Fouls are much more common at the rim.
    foul_chance = (
        0.085
        + (shooter.offense - 50) / 900.0
        + (off.offense_coach - 50) / 1400.0
        - (def_def - 50) / 1200.0
        + fatigue_pen * 0.05
        + (0.012 if clutch else 0.0)
    )
    # Foul tuning: keep global at 0.95, but shift fouls toward 2PT contact.
    foul_mult_global = 0.95
    foul_mult_2pt = 1.52

    # Shot-type adjustment:
    # - rim: slightly more fouls
    # - mid: fewer fouls
    foul_mult_2pt *= 1.12 if is_rim else 0.85

    foul_chance *= foul_mult_global * foul_mult_2pt

    # Star bias is stronger on 2s (pressure at the rim).
    foul_bias = 1.0 + (shooter.offense - 80) / 200.0
    foul_bias = clamp(foul_bias, 0.85, 1.20)
    foul_chance *= foul_bias
    foul_chance = clamp(foul_chance, 0.035, 0.18)
    fouled = random.random() < foul_chance

    if made:
        points = 2
        shooter.box.fgm += 1
        shooter.box.pts += 2

        # and-1 FT
        if fouled:
            shooter.box.fta += 1
            if random.random() < ft_make_prob(shooter):
                shooter.box.ftm += 1
                shooter.box.pts += 1
                points += 1

            fouler = random.choices(deff.starters, weights=[p.defense for p in deff.starters], k=1)[0]
            fouler.box.pf += 1

        if random.random() < clamp(0.54 + (off_iq - 50) / 170.0, 0.28, 0.78):
            passers = [p for p in off.starters if p is not shooter]
            passer = random.choices(passers, weights=[p.iq for p in passers], k=1)[0]
            passer.box.ast += 1
        return points
    else:
        # Shooting foul -> 2 free throws on miss
        if fouled:
            fouler = random.choices(deff.starters, weights=[p.defense for p in deff.starters], k=1)[0]
            fouler.box.pf += 1

            shooter.box.fta += 2
            ft_prob = ft_make_prob(shooter)
            made_fts = 0
            for _ in range(2):
                if random.random() < ft_prob:
                    shooter.box.ftm += 1
                    shooter.box.pts += 1
                    made_fts += 1
            return made_fts

        # Blocks occur on missed 2s.
        blk_chance = clamp(0.040 + (def_def - 50) / 520.0 - (shooter.offense - 50) / 1200.0, 0.010, 0.11)
        if random.random() < blk_chance:
            blocker = random.choices(
                deff.starters,
                weights=[p.defense * 0.8 + p.stamina * 0.2 for p in deff.starters],
                k=1,
            )[0]
            blocker.box.blk += 1

        rebounder = random.choices(
            off.starters + deff.starters,
            weights=[
                (p.defense + p.stamina) * (1.06 if is_rim and p in off.starters else 1.0)
                for p in off.starters + deff.starters
            ],
            k=1,
        )[0]
        rebounder.box.reb += 1
        return 0


def simulate_game(home: Team, away: Team, pace: int = 108, bench_tax: float = 0.18) -> GameResult:
    """
    bench_tax: share of possessions that go to bench/dead minutes.
    Keeps scores realistic while only tracking 5 starters.
    """
    reset_box(home)
    reset_box(away)

    # Initialize per-game takeover flags (only one per team per game)
    home._takeover_triggered = False
    away._takeover_triggered = False
    home._takeover_player = None
    away._takeover_player = None

    home_pts = 0
    away_pts = 0

    base_q_poss = pace // 4
    extra = pace % 4
    for q in range(1, 5):
        q_poss = base_q_poss + (1 if q <= extra else 0)
        for _ in range(q_poss):
            clutch = (q == 4 and abs(home_pts - away_pts) <= 8)

            # Blowout pacing: slow the game late when the margin is big.
            # We model this as extra "dead minutes" (bench possessions) in Q4.
            effective_bench_tax = bench_tax
            if q == 4 and abs(home_pts - away_pts) >= 18:
                effective_bench_tax = clamp(bench_tax + 0.12, 0.0, 0.45)

                # Also reduce effective pace by burning clock on some possessions.
                # This helps prevent late blowouts from spiraling into 140+ point endings.
                if random.random() < 0.30:
                    continue

            # High-total slowdown: if the game is already extremely high-scoring,
            # burn a bit of clock in Q4 to keep 140+ team scores rare.
            if q == 4 and (home_pts + away_pts) >= 230:
                effective_bench_tax = clamp(effective_bench_tax + 0.05, 0.0, 0.50)
                if random.random() < 0.10:
                    continue

            if random.random() > effective_bench_tax:
                home_pts += simulate_possession(home, away, q, clutch)
            else:
                home_pts += simulate_bench_possession(home, away, q, clutch)

            clutch = (q == 4 and abs(home_pts - away_pts) <= 8)

            if random.random() > effective_bench_tax:
                away_pts += simulate_possession(away, home, q, clutch)
            else:
                away_pts += simulate_bench_possession(away, home, q, clutch)

    # Overtime: only if tied after regulation.
    # Requirements:
    # - 12 total possessions per OT (6 per team)
    # - no bench_tax reduction
    # - clutch=True on all OT possessions
    ot_periods = 0
    while home_pts == away_pts:
        ot_periods += 1
        ot_quarter = 4 + ot_periods
        for _ in range(6):
            home_pts += simulate_possession(home, away, ot_quarter, True)
            away_pts += simulate_possession(away, home, ot_quarter, True)

    total_possessions = pace + ot_periods * 12
    result = GameResult(home=home, away=away, home_pts=home_pts, away_pts=away_pts, possessions=total_possessions)
    if ot_periods > 0:
        # Attach simple metadata without changing the GameResult dataclass.
        # Downstream code can read `result.meta` if it wants to display OT.
        setattr(result, "meta", "(OT)")
        setattr(result, "ot_periods", ot_periods)
    return result

