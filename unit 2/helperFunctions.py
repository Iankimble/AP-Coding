import pandas as pd

def get_team_records(year):
    games = nfl.import_schedules([year])

    if "season_type" in games.columns:
        games = games[games["season_type"] == "REG"]
    else:
        games = games[games["game_type"] == "REG"]

    games = games.dropna(subset=["home_score", "away_score"])

    home = games[["home_team", "home_score", "away_score"]].rename(
        columns={"home_team": "team", "home_score": "points_for", "away_score": "points_against"}
    )
    home["win"] = (home["points_for"] > home["points_against"]).astype(int)

    away = games[["away_team", "away_score", "home_score"]].rename(
        columns={"away_team": "team", "away_score": "points_for", "home_score": "points_against"}
    )
    away["win"] = (away["points_for"] > away["points_against"]).astype(int)

    all_games = pd.concat([home, away])

    records = all_games.groupby("team").agg(
        wins=("win", "sum"),
        losses=("win", lambda x: len(x) - x.sum()),
        points_for=("points_for", "sum"),
        points_against=("points_against", "sum")
    ).reset_index()

    records = records.sort_values("wins", ascending=False).reset_index(drop=True)

    return records

def get_season_Results_By_team(year, team):
    schedules = nfl.import_schedules([year])

    if "season_type" in schedules.columns:
        schedules = schedules[schedules["season_type"] == "REG"]
    else:
        schedules = schedules[schedules["game_type"] == "REG"]

    team_games = schedules[
        (schedules["home_team"] == team) | (schedules["away_team"] == team)
    ].copy()

    def get_result(row):
        if row["home_team"] == team:
            return "W" if row["home_score"] > row["away_score"] else "L"
        else:
            return "W" if row["away_score"] > row["home_score"] else "L"

    team_games["result"] = team_games.apply(get_result, axis=1)
    team_games["points_for"] = team_games.apply(
        lambda r: r["home_score"] if r["home_team"] == team else r["away_score"], axis=1
    )
    team_games["points_against"] = team_games.apply(
        lambda r: r["away_score"] if r["home_team"] == team else r["home_score"], axis=1
    )

    return team_games[["week", "home_team", "away_team", "points_for", "points_against", "result"]]

def weeklyPlayerStats(year, position, week=None):
    """
    Get season or single-week stats by player for a position.

    Args:
        year (int): NFL season (e.g., 2024)
        position (str): 'QB', 'RB', 'FB', 'WR', 'TE', etc.
        week (int|list[int]|None): specific week or list of weeks; None = all weeks

    Returns:
        pandas.DataFrame: aggregated stats sorted by the primary yardage stat for that position
    """
    weekly = nfl.import_weekly_data([year])

    # --- normalize inputs ---
    pos = str(position).upper()

    # --- optional week filter ---
    if week is not None:
        if isinstance(week, (list, tuple, set)):
            weekly = weekly[weekly["week"].isin(list(week))]
        else:
            weekly = weekly[weekly["week"] == int(week)]

    # --- filter by position (handle NaN) ---
    filtered = weekly[weekly["position"].fillna("").str.upper() == pos].copy()

    # --- choose team column (keep your output as 'recent_team') ---
    team_col = "recent_team" if "recent_team" in filtered.columns else ("team" if "team" in filtered.columns else None)
    if team_col is None:
        team_col = "recent_team"
        filtered[team_col] = pd.NA

    # --- alias map: pick whatever exists in the data safely ---
    aliases = {
        "pass_yards":      ["passing_yards", "pass_yards"],
        "pass_tds":        ["passing_tds", "pass_tds", "pass_td"],
        "pass_att":        ["pass_attempts", "passing_attempts", "attempts"],
        "pass_cmp":        ["completions", "pass_completions", "passing_completions"],
        "interceptions":   ["interceptions", "pass_interceptions", "int"],
        "rush_yards":      ["rushing_yards", "rush_yards"],
        "rush_tds":        ["rushing_tds", "rush_tds"],
        "rush_att":        ["rushing_attempts", "rush_att", "carries"],
        "rec_yards":       ["receiving_yards", "rec_yards"],
        "rec_tds":         ["receiving_tds", "rec_tds"],
        "receptions":      ["receptions", "rec"],
        "targets":         ["targets", "tar"],
        "fantasy_points":  ["fantasy_points", "fantasy_points_ppr", "fantasy_points_half_ppr"],
    }

    def ensure_col(df, key):
        """Return the actual column name present for a logical key; create zeros if missing."""
        for cand in aliases.get(key, [key]):
            if cand in df.columns:
                return cand
        # create a zero column if truly missing
        df[key] = 0
        return key

    # resolve the columns against the actual dataset
    cols = {k: ensure_col(filtered, k) for k in aliases.keys()}

    # --- pick metrics by position (kept simple, add both primary + common secondaries) ---
    if pos == "QB":
        agg_cols = [cols["pass_yards"], cols["pass_tds"], cols["pass_att"], cols["pass_cmp"],
                    cols["interceptions"], cols["rush_yards"], cols["rush_tds"], cols["fantasy_points"]]
        primary_sort = cols["pass_yards"]
    elif pos in ("RB", "FB"):
        agg_cols = [cols["rush_yards"], cols["rush_tds"], cols["rush_att"],
                    cols["rec_yards"], cols["receptions"], cols["rec_tds"], cols["fantasy_points"]]
        primary_sort = cols["rush_yards"]
    elif pos in ("WR", "TE"):
        agg_cols = [cols["rec_yards"], cols["receptions"], cols["rec_tds"],
                    cols["rush_yards"], cols["rush_tds"], cols["fantasy_points"]]
        primary_sort = cols["rec_yards"]
    else:
        # generic bundle
        agg_cols = [cols["fantasy_points"], cols["rec_yards"], cols["receptions"],
                    cols["rush_yards"], cols["rush_tds"], cols["pass_yards"]]
        primary_sort = cols["fantasy_points"]

    # make numeric & safe for sum
    for c in set(agg_cols):
        filtered[c] = pd.to_numeric(filtered[c], errors="coerce").fillna(0)

    # --- aggregate ---
    stats = (
        filtered.groupby(["player_id", "player_name", team_col], dropna=False)[agg_cols]
        .sum(min_count=1)
        .reset_index()
        .rename(columns={team_col: "recent_team"})
        .sort_values(primary_sort, ascending=False)
    )

    # --- derived rates (added after aggregation so rates are season/week-aggregated) ---
    # Completion %
    if {cols["pass_att"], cols["pass_cmp"]}.issubset(stats.columns):
        with pd.option_context('mode.use_inf_as_na', True):
            stats["cmp_pct"] = (stats[cols["pass_cmp"]] / stats[cols["pass_att"]]).replace([pd.NA], 0) * 100

    # Y/A
    if {cols["pass_yards"], cols["pass_att"]}.issubset(stats.columns):
        with pd.option_context('mode.use_inf_as_na', True):
            stats["pass_ya"] = (stats[cols["pass_yards"]] / stats[cols["pass_att"]]).replace([pd.NA], 0)

    # YPC
    if {cols["rush_yards"], cols["rush_att"]}.issubset(stats.columns):
        with pd.option_context('mode.use_inf_as_na', True):
            stats["rush_ypc"] = (stats[cols["rush_yards"]] / stats[cols["rush_att"]]).replace([pd.NA], 0)

    # YPR
    if {cols["rec_yards"], cols["receptions"]}.issubset(stats.columns):
        with pd.option_context('mode.use_inf_as_na', True):
            stats["rec_ypr"] = (stats[cols["rec_yards"]] / stats[cols["receptions"]]).replace([pd.NA], 0)

    # keep most relevant columns first
    front_cols = ["player_id", "player_name", "recent_team"]
    ordered = front_cols + [c for c in agg_cols if c in stats.columns] + [c for c in ["cmp_pct","pass_ya","rush_ypc","rec_ypr"] if c in stats.columns]
    stats = stats[ordered]

    return stats

