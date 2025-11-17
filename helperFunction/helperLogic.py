import pandas as pd
import nfl_data_py as nfl
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
from typing import Union, Tuple

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

def _resolve_col(df: pd.DataFrame, col_name: str) -> str:
    """Return the exact dataframe column matching col_name (case-insensitive)."""
    lookup = {c.lower(): c for c in df.columns}
    key = str(col_name).strip().lower()
    if key in lookup:
        return lookup[key]
    # helpful error showing a few options
    raise KeyError(
        f"Column '{col_name}' not found. Available columns include: "
        + ", ".join(list(df.columns)[:30])
        + (" ..." if len(df.columns) > 30 else "")
    )

def plot_player_stat(
    stats: pd.DataFrame,
    stat: str,
    top_n: int = 15,
    title: str | None = None,
    annotate: bool = True,
    figsize=(10, 6),
    save_path: str | None = None,
):
    """
    Plot a horizontal bar chart from a weeklyPlayerStats dataframe for the chosen stat column.

    Args:
        stats (pd.DataFrame): output of weeklyPlayerStats(...)
        stat (str): column name in `stats` to plot (case-insensitive)
        top_n (int): number of players to show
        title (str|None): optional chart title
        annotate (bool): write values at the end of bars
        figsize (tuple): figure size
        save_path (str|None): if provided, save the figure to this path

    Returns:
        matplotlib.axes.Axes, pd.DataFrame (the data actually plotted)
    """
    # resolve column and coerce numeric
    stat_col = _resolve_col(stats, stat)
    df = stats.copy()

    # Build a readable label "Player (TEAM)"
    team_col = "recent_team" if "recent_team" in df.columns else None
    if team_col is None:
        # try common alternates, else blank
        for cand in ("team", "posteam", "recent_team"):
            if cand in df.columns:
                team_col = cand
                break
    team_col = team_col or "recent_team"
    if team_col not in df.columns:
        df[team_col] = ""

    df["label"] = (
        df.get("player_name", pd.Series([""] * len(df))).fillna("")
        + " ("
        + df[team_col].fillna("")
        + ")"
    ).str.strip()

    # numeric & drop missing
    df[stat_col] = pd.to_numeric(df[stat_col], errors="coerce")
    plot_df = df.dropna(subset=[stat_col]).sort_values(stat_col, ascending=False).head(top_n)

    # Basic plot
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(plot_df["label"], plot_df[stat_col])
    ax.invert_yaxis()  # highest at top

    # Labels & title
    ax.set_xlabel(stat_col)
    ax.set_ylabel("Player")
    if title is None:
        title = f"Top {min(top_n, len(plot_df))} by {stat_col}"
    ax.set_title(title)

    # Annotations
    if annotate:
        is_pct = "pct" in stat_col.lower()  # e.g., cmp_pct
        for i, v in enumerate(plot_df[stat_col].to_numpy()):
            txt = f"{v:.1f}%" if is_pct else f"{v:.0f}" if float(v).is_integer() else f"{v:.2f}"
            ax.text(v, i, f"  {txt}", va="center")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")

    return ax, plot_df

def plot_weekly_player_stats(
    year: int,
    position: str,
    stat: str,
    week=None,
    **plot_kwargs,
):
    """
    Convenience wrapper: runs weeklyPlayerStats(year, position, week) then plots `stat`.
    plot_kwargs are forwarded to plot_player_stat (top_n, title, annotate, figsize, save_path).
    """
    stats = weeklyPlayerStats(year, position, week=week)
    return plot_player_stat(stats, stat=stat, **plot_kwargs)

def get_position_columns(year: int = 2024, position: str = "QB") -> list[str]:
    """
    Return all available stat columns for a given position.

    Args:
        year (int): NFL season (default=2024)
        position (str): Player position, e.g. "QB", "WR", "RB", "TE"

    Returns:
        list[str]: Sorted list of column names available for that position.
    """
    # Load weekly data
    weekly = nfl.import_weekly_data([year])
    
    # Normalize position
    pos = str(position).upper()
    
    # Filter by position (handle missing data)
    filtered = weekly[weekly["position"].fillna("").str.upper() == pos]
    
    # If no data found for that position, warn and return all columns
    if filtered.empty:
        print(f"⚠️ No data found for position '{pos}' in {year}. Returning all columns.")
        return sorted(list(weekly.columns))
    
    # Return sorted list of columns for that position
    return sorted(list(filtered.columns))

def get_player_stats_by_name(
    year: int,
    player_name: str,
    position: str,
    week: int | list[int] | None = None,
    exact: bool = False,
) -> pd.DataFrame:
    """
    Look up a single player's aggregated stats for a given year (and optional week[s]),
    using the existing weeklyPlayerStats helper.

    Args:
        year (int): NFL season (e.g., 2024)
        player_name (str): Name or partial name of the player, e.g. "Jalen Hurts"
        position (str): Player position (e.g., "QB", "RB", "WR", "TE")
        week (int|list[int]|None): Single week, list of weeks, or None for full season
        exact (bool): 
            - True  -> match full name exactly (case-insensitive)
            - False -> substring / partial match (case-insensitive)

    Returns:
        pandas.DataFrame: Filtered stats for the matching player(s).
                         Same columns/structure as weeklyPlayerStats output.

    Raises:
        ValueError: If no players match the given name.
    """
    # reuse your existing logic to get aggregated stats by player
    stats = weeklyPlayerStats(year, position, week=week)

    # normalize search
    name_query = player_name.strip().lower()

    if exact:
        mask = stats["player_name"].str.lower() == name_query
    else:
        mask = stats["player_name"].str.contains(name_query, case=False, na=False)

    result = stats[mask].copy()

    if result.empty:
        raise ValueError(
            f"No players found matching name '{player_name}' "
            f"for year {year} and position {position}."
        )

    # Optional: keep the same ordering weeklyPlayerStats already has
    # or sort by fantasy_points if present:
    if "fantasy_points" in result.columns:
        result = result.sort_values("fantasy_points", ascending=False)

    return result

def get_advanced_team_records(year: int, return_game_level: bool = False
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Get team records plus advanced team performance stats.

    Args:
        year (int): NFL season (e.g., 2024)
        return_game_level (bool): 
            False  -> return only team summary records (default, backwards compatible)
            True   -> return (team_records, team_game_stats) where team_game_stats is
                      per-team-per-game with metadata and advanced stats.

    Returns:
        pandas.DataFrame OR (pandas.DataFrame, pandas.DataFrame):
            - records: one row per team with wins, losses, PF/PA, point diff, etc.
            - team_games (optional): one row per team-game with metadata + advanced stats
    """

    # -------------------------
    # 1. Load schedule / games
    # -------------------------
    games = nfl.import_schedules([year])

    # Regular season filter (handles schema differences)
    if "season_type" in games.columns:
        games = games[games["season_type"] == "REG"]
    else:
        games = games[games["game_type"] == "REG"]

    # Completed games only
    games = games.dropna(subset=["home_score", "away_score"])

    # Basic W/L flags at game level
    games["home_win"] = (games["home_score"] > games["away_score"]).astype(int)
    games["away_win"] = (games["away_score"] > games["home_score"]).astype(int)

    # -------------------------
    # 2. Game metadata subset
    # -------------------------
    # These columns may vary by version; we only keep ones that exist.
    meta_cols = [
        "game_id", "week", "gameday", "weekday", "gametime",
        "stadium", "roof", "surface", "temp", "wind",
        "spread_line", "total_line",
        "home_team", "away_team", "home_score", "away_score"
    ]
    existing_meta_cols = [c for c in meta_cols if c in games.columns]
    games_meta = games[existing_meta_cols].copy()

    # --------------------------------------------
    # 3. Build per-team-per-game basic stat table
    # --------------------------------------------
    # Home rows
    home = pd.DataFrame({
        "game_id": games["game_id"],
        "week": games["week"],
        "team": games["home_team"],
        "opponent": games["away_team"],
        "points_for": games["home_score"],
        "points_against": games["away_score"],
        "win": games["home_win"],
        "location": "home"
    })

    # Away rows
    away = pd.DataFrame({
        "game_id": games["game_id"],
        "week": games["week"],
        "team": games["away_team"],
        "opponent": games["home_team"],
        "points_for": games["away_score"],
        "points_against": games["home_score"],
        "win": games["away_win"],
        "location": "away"
    })

    team_games_basic = pd.concat([home, away], ignore_index=True)

    # --------------------------------------
    # 4. Load play-by-play & build advanced
    # --------------------------------------
    # Limit to needed columns to keep memory sane
    pbp_cols = [
        "play_id",
        "game_id",
        "posteam",      # offensive team
        "defteam",
        "yards_gained",
        "rush_attempt",
        "pass_attempt",
        "passing_yards",
        "rushing_yards",
        "epa",
        "success",
        "interception",
        "fumble_lost",
        "touchdown"
    ]

    pbp = nfl.import_pbp_data([year], columns=pbp_cols)

    # Keep only offensive plays that have a posteam
    pbp = pbp[~pbp["posteam"].isna()].copy()

    team_game_advanced = (
        pbp.groupby(["game_id", "posteam"])
           .agg(
               plays=("play_id", "count"),
               total_yards=("yards_gained", "sum"),
               passing_yards=("passing_yards", "sum"),
               rushing_yards=("rushing_yards", "sum"),
               rush_attempts=("rush_attempt", "sum"),
               pass_attempts=("pass_attempt", "sum"),
               total_epa=("epa", "sum"),
               avg_epa=("epa", "mean"),
               success_rate=("success", "mean"),
               interceptions=("interception", "sum"),
               fumbles_lost=("fumble_lost", "sum"),
               touchdowns=("touchdown", "sum"),
           )
           .reset_index()
    )

    team_game_advanced["turnovers"] = (
        team_game_advanced["interceptions"] + team_game_advanced["fumbles_lost"]
    )

    # -----------------------------------------
    # 5. Merge basic team-games with advanced
    # -----------------------------------------
    team_games = team_games_basic.merge(
        team_game_advanced,
        left_on=["game_id", "team"],
        right_on=["game_id", "posteam"],
        how="left"
    ).drop(columns=["posteam"])

    # Add game metadata (stadium, roof, temp, spread, etc.)
    team_games = team_games.merge(
        games_meta,
        on="game_id",
        how="left",
        suffixes=("", "_meta")
    )

    # -----------------------------------------
    # 6. Aggregate to team-level records
    # -----------------------------------------
    records = (
        team_games.groupby("team")
        .agg(
            games_played=("win", "count"),
            wins=("win", "sum"),
            losses=("win", lambda x: len(x) - x.sum()),
            points_for=("points_for", "sum"),
            points_against=("points_against", "sum"),
            point_diff=("points_for", lambda x: x.sum())  # temp placeholder
        )
        .reset_index()
    )

    # Fix point differential & add win%
    records["point_diff"] = records["points_for"] - records["points_against"]
    records["win_pct"] = records["wins"] / records["games_played"]

    # Add some aggregated advanced metrics
    advanced_team_agg = (
        team_games.groupby("team")
        .agg(
            total_yards=("total_yards", "sum"),
            passing_yards=("passing_yards", "sum"),
            rushing_yards=("rushing_yards", "sum"),
            plays=("plays", "sum"),
            total_epa=("total_epa", "sum"),
            avg_epa=("avg_epa", "mean"),
            success_rate=("success_rate", "mean"),
            turnovers=("turnovers", "sum")
        )
        .reset_index()
    )

    records = records.merge(advanced_team_agg, on="team", how="left")

    # Sort like before
    records = records.sort_values(
        ["wins", "point_diff"], ascending=[False, False]
    ).reset_index(drop=True)

    if return_game_level:
        # records: one row per team
        # team_games: one row per team per game with meta + advanced stats
        return records, team_games

    return records

def compare_two_teams_points(team_games, team_a, team_b):
    data_a = team_games[team_games["team"] == team_a].sort_values("week")
    data_b = team_games[team_games["team"] == team_b].sort_values("week")

    plt.figure(figsize=(10, 6))
    plt.plot(data_a["week"], data_a["points_for"], marker="o", label=team_a)
    plt.plot(data_b["week"], data_b["points_for"], marker="o", label=team_b)

    plt.title(f"{team_a} vs {team_b} – Points by Week")
    plt.xlabel("Week")
    plt.ylabel("Points Scored")
    plt.xticks(sorted(team_games["week"].unique()))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_team_points_by_week(team_games, team):
    data = team_games[team_games["team"] == team].sort_values("week")

    plt.figure(figsize=(10, 6))
    plt.plot(data["week"], data["points_for"], marker="o")
    plt.title(f"{team} Points For by Week")
    plt.xlabel("Week")
    plt.ylabel("Points Scored")
    plt.xticks(data["week"])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_point_diff_vs_win_pct(records):
    plt.figure(figsize=(10, 6))
    plt.scatter(records["point_diff"], records["win_pct"])

    for _, row in records.iterrows():
        plt.text(row["point_diff"], row["win_pct"], row["team"],
                 fontsize=8, ha="center", va="bottom")

    plt.title("Point Differential vs Win Percentage")
    plt.xlabel("Point Differential (Points For - Points Against)")
    plt.ylabel("Win Percentage")
    plt.axvline(0, linestyle="--")
    plt.tight_layout()
    plt.show()
