import nfl_data_py as nfl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_season_totals_by_position(year: int, position: str) -> pd.DataFrame:
    """
    Return trimmed full-season stats for all players at a given position.

    Args:
        year (int): NFL season (e.g., 2024)
        position (str): Player position ('QB', 'RB', 'WR', 'TE', etc.)

    Returns:
        pandas.DataFrame: One row per player with core season-total stats.
    """
    # Load weekly stats for the season
    weekly = nfl.import_weekly_data([year])

    pos = position.upper()

    if "position" not in weekly.columns:
        raise ValueError("Column 'position' not found in weekly data.")

    # Filter to the requested position
    pos_df = weekly[weekly["position"] == pos].copy()
    if pos_df.empty:
        raise ValueError(f"No data found for position '{pos}' in season {year}.")

    # Identify player columns
    group_cols = ["player_display_name", "player_id", "position", "recent_team"]
    group_cols = [c for c in group_cols if c in pos_df.columns]

    # Calculate games played per player
    if "week" in pos_df.columns:
        games_played = (
            pos_df.groupby(group_cols)["week"]
            .nunique()
            .reset_index(name="games_played")
        )
    else:
        # Fallback if week isn't available
        games_played = (
            pos_df.groupby(group_cols)
            .size()
            .reset_index(name="games_played")
        )

    # Numeric columns to sum
    numeric_cols = pos_df.select_dtypes(include="number").columns.tolist()
    # Remove fantasy-related columns
    fantasy_cols = [c for c in numeric_cols if "fantasy" in c.lower()]
    numeric_cols = [c for c in numeric_cols if c not in fantasy_cols]

    # Group by player and sum
    season_totals = (
        pos_df[group_cols + numeric_cols]
        .groupby(group_cols, as_index=False)[numeric_cols]
        .sum()
    )

    # Merge games_played
    season_totals = season_totals.merge(games_played, on=group_cols, how="left")

    # ---- Position-specific core columns ----
    core_stats_by_pos = {
        "QB": [
            "games_played",
            "attempts",
            "completions",
            "passing_yards",
            "passing_tds",
            "interceptions",
            "rushing_yards",
            "rushing_tds",
        ],
        "RB": [
            "games_played",
            "rushing_attempts",
            "rushing_yards",
            "rushing_tds",
            "targets",
            "receptions",
            "receiving_yards",
            "receiving_tds",
        ],
        "WR": [
            "games_played",
            "targets",
            "receptions",
            "receiving_yards",
            "receiving_tds",
        ],
        "TE": [
            "games_played",
            "targets",
            "receptions",
            "receiving_yards",
            "receiving_tds",
        ],
    }

    # Choose which columns to keep
    base_cols = group_cols.copy()
    pos_core = core_stats_by_pos.get(pos, ["games_played"])
    keep_cols = base_cols + [c for c in pos_core if c in season_totals.columns]

    # Filter to trimmed set of columns
    season_totals = season_totals[keep_cols]

    # Sort by a key stat depending on position
    if pos == "QB" and "passing_yards" in season_totals.columns:
        season_totals = season_totals.sort_values("passing_yards", ascending=False)
    elif pos == "RB" and "rushing_yards" in season_totals.columns:
        season_totals = season_totals.sort_values("rushing_yards", ascending=False)
    elif pos in ("WR", "TE") and "receiving_yards" in season_totals.columns:
        season_totals = season_totals.sort_values("receiving_yards", ascending=False)

    return season_totals

#qb_2024_totals_top5 = get_season_totals_by_position(2024, "QB")
#print(qb_2024_totals_top5.head())
#qb_2024 = get_season_totals_by_position(2024, "QB")
#print(qb_2024)

def plot_position_stat_bar(year: int,
                           position: str,
                           stat_col: str,
                           top_n: int = 20,
                           save_path: str = None) -> None:
    """
    Plot a bar chart for a given stat column for all players at a position,
    and optionally save it as a PNG file.

    Args:
        year (int): NFL season (e.g., 2024)
        position (str): Position (e.g., 'QB', 'RB', 'WR', 'TE')
        stat_col (str): Stat column to plot (e.g., 'passing_yards')
        top_n (int): Show top N players (default 20)
        save_path (str): Optional. File path to save PNG (e.g., 'qb_passing_2024.png')

    Returns:
        None
    """
    df = get_season_totals_by_position(year, position)

    if stat_col not in df.columns:
        raise ValueError(
            f"Column '{stat_col}' not found. Available columns: {list(df.columns)}"
        )

    df_sorted = df.sort_values(stat_col, ascending=False).head(top_n)

    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted["player_display_name"], df_sorted[stat_col])

    pretty_stat = stat_col.replace("_", " ").title()
    plt.title(f"Top {top_n} {position.upper()} by {pretty_stat} in {year}")
    plt.xlabel("Player")
    plt.ylabel(pretty_stat)
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    # --- 🔥 Save chart if save_path is given ---
    if save_path:
        plt.savefig(save_path, dpi=300)  # dpi=300 gives high quality images
        print(f"Chart saved as: {save_path}")

    plt.show()

# plot_position_stat_bar(2024, "QB", "passing_yards", save_path="qb_passing_2024.png", top_n=20)
# plot_position_stat_bar(2024, "RB", "rushing_yards", save_path="rb_rushing_2024.png", top_n=20)

def get_player_stats(year: int, first_name: str, last_name: str) -> pd.DataFrame:
    """
    Get all weekly stats for a single NFL player for a given season.
    Requires exact match on first and last name.

    Args:
        year (int): NFL season year (e.g., 2024)
        first_name (str): Player's first name (e.g., "Jalen")
        last_name (str): Player's last name (e.g., "Hurts")

    Returns:
        pandas.DataFrame: All weekly stats for that player in that season.
    """

    # Load weekly data for the season
    weekly = nfl.import_weekly_data([year])

    # Normalize inputs
    first = first_name.lower().strip()
    last = last_name.lower().strip()

    # Normalize player names in the dataset
    weekly["first"] = weekly["player_display_name"].str.split().str[0].str.lower()
    weekly["last"] = weekly["player_display_name"].str.split().str[-1].str.lower()

    # Exact match on first + last
    player_df = weekly[(weekly["first"] == first) & (weekly["last"] == last)].copy()

    if player_df.empty:
        raise ValueError(
            f"No data found for player '{first_name} {last_name}' in season {year}."
        )

    # Sort by week for clean output
    player_df = player_df.sort_values("week")

    # Remove temporary helper columns
    player_df = player_df.drop(columns=["first", "last"], errors="ignore")

    return player_df

# playerData= get_player_stats(2024, 'Lamar','Jackson')
# print(playerData)

def dataframe_to_png(df, png_path="dataframe.png", fontsize=10, col_width=2.0):
    """
    Save a pandas DataFrame as a PNG image using Matplotlib.

    Args:
        df (pd.DataFrame): The DataFrame to export
        png_path (str): File path to save the PNG
        fontsize (int): Font size in the table
        col_width (float): Width of each column in the image

    Returns:
        None (saves PNG file)
    """

    # Calculate figure size based on rows and columns
    n_rows, n_cols = df.shape
    figsize = (col_width * n_cols, 0.4 * n_rows)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")  # hide axes

    # Create table
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(1, 1.5)  # increase row height

    # Save image
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"DataFrame saved as PNG: {png_path}")

# qb_totals = get_season_totals_by_position(2024, "QB")

# dataframe_to_png(qb_totals, "qb_totals_2024.png")

def export_player_season_png(
    year: int,
    first_name: str,
    last_name: str,
    png_path: str | None = None,
    columns: list[str] | None = None,
    fontsize: int = 10,
) -> str:
    """
    Get a player's weekly stats for a season and export them as a PNG table.

    Args:
        year (int): NFL season (e.g., 2024)
        first_name (str): Player's first name (e.g., "Jalen")
        last_name (str): Player's last name (e.g., "Hurts")
        png_path (str | None): Optional file path for the PNG.
                               If None, a name is generated automatically.
        columns (list[str] | None): Optional list of columns to include.
                                    If None, all columns are used.
        fontsize (int): Font size for the table text.

    Returns:
        str: The path to the saved PNG file.
    """

    # 1. Get the player's DataFrame (one row per week)
    df = get_player_stats(year, first_name, last_name)

    # 2. Keep only selected columns if provided
    if columns is not None:
        # Only keep columns that exist in df
        cols_to_use = [c for c in columns if c in df.columns]
        if not cols_to_use:
            raise ValueError("None of the specified columns exist in the DataFrame.")
        df = df[cols_to_use]

    # 3. Auto-generate a file name if not provided
    if png_path is None:
        safe_first = first_name.lower().replace(" ", "_")
        safe_last = last_name.lower().replace(" ", "_")
        png_path = f"{safe_first}_{safe_last}_{year}_stats.png"

    # 4. Build the table figure
    n_rows, n_cols = df.shape
    # Reasonable sizing for a single player season (usually <= 18 games)
    figsize = (max(8, n_cols * 1.2), max(2, n_rows * 0.6))

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(1, 1.4)  # increase row height a bit

    # 5. Add a title
    full_name = f"{first_name} {last_name}"
    ax.set_title(f"{full_name} – {year} Season Stats (Weekly)", pad=20)

    # 6. Save as PNG
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close(fig)

    print(f"Saved player stats table as: {png_path}")
    return png_path

# export_player_season_png(2024, "Jalen", "Hurts")

def plot_player_stat_by_week(
    year: int,
    first_name: str,
    last_name: str,
    stat_col: str,
    save_path: str | None = None
) -> None:
    """
    Plot a line graph for a specific player's stat by week for a given season.

    Args:
        year (int): NFL season year (e.g., 2024)
        first_name (str): Player's first name (e.g., "Jalen")
        last_name (str): Player's last name (e.g., "Hurts")
        stat_col (str): Column name of the stat to plot
                        (e.g., "passing_yards", "rushing_yards", "receiving_yards")
        save_path (str | None): Optional path to save the plot as a PNG.
                                If None, the plot is just shown.

    Returns:
        None
    """

    # Get the player's weekly stats DataFrame (using the helper we wrote earlier)
    df = get_player_stats(year, first_name, last_name)

    # Make sure the stat column exists
    if stat_col not in df.columns:
        raise ValueError(
            f"Column '{stat_col}' not found in player data. "
            f"Available columns include: {list(df.columns)}"
        )

    # Ensure data is sorted by week
    if "week" not in df.columns:
        raise ValueError("Column 'week' not found in player data.")
    df = df.sort_values("week")

    # Convert the stat column to numeric (just in case) and fill NaN with 0
    df[stat_col] = pd.to_numeric(df[stat_col], errors="coerce").fillna(0)

    weeks = df["week"]
    values = df[stat_col]

    # Create the line plot
    plt.figure(figsize=(10, 5))
    plt.plot(weeks, values, marker="o")

    # Labels and title
    pretty_stat = stat_col.replace("_", " ").title()
    full_name = f"{first_name} {last_name}"

    plt.title(f"{full_name} – {pretty_stat} by Week ({year} Season)")
    plt.xlabel("Week")
    plt.ylabel(pretty_stat)
    plt.xticks(weeks)  # show actual week numbers on x-axis
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    # Optionally save as PNG
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved line chart as: {save_path}")

    # Show the plot
    plt.show()

# plot_player_stat_by_week(
#    2004,
#    "Brian",
#    "Westbrook",
#    "rushing_yards",
#    save_path="brian_westbrook_2004_rushing_yards_by_week.png"
# ) 

def get_team_season_data(year: int, include_team_meta: bool = True) -> pd.DataFrame:
    """
    Get clean team-level season stats for all teams for a given NFL season.
    
    Removes ALL metadata fields related to:
        - logos
        - colors
        - wordmarks
        - nicknames
        - divisions

    Adds:
        - points_for
        - points_against
        - point_diff
        - ppg_for
        - ppg_against

    Compatible with nfl_data_py 0.3.3.
    """

    # 1. Load schedule data
    games = nfl.import_schedules([year])

    if "season_type" in games.columns:
        games = games[games["season_type"] == "REG"]

    games = games.dropna(subset=["home_score", "away_score"])

    # 2. Build home and away rows
    home = games[["home_team", "home_score", "away_score"]].rename(
        columns={"home_team": "team", "home_score": "points_for", "away_score": "points_against"}
    )
    away = games[["away_team", "away_score", "home_score"]].rename(
        columns={"away_team": "team", "away_score": "points_for", "home_score": "points_against"}
    )

    # Outcomes
    for df in (home, away):
        df["win"] = (df["points_for"] > df["points_against"]).astype(int)
        df["loss"] = (df["points_for"] < df["points_against"]).astype(int)
        df["tie"]  = (df["points_for"] == df["points_against"]).astype(int)

    # Combine
    team_games = pd.concat([home, away], ignore_index=True)

    # 3. Aggregate season totals
    team_stats = team_games.groupby("team").agg(
        games_played=("win", "size"),
        wins=("win", "sum"),
        losses=("loss", "sum"),
        ties=("tie", "sum"),
        points_for=("points_for", "sum"),
        points_against=("points_against", "sum")
    ).reset_index()

    # Derived stats
    team_stats["point_diff"] = team_stats["points_for"] - team_stats["points_against"]
    team_stats["ppg_for"] = team_stats["points_for"] / team_stats["games_played"]
    team_stats["ppg_against"] = team_stats["points_against"] / team_stats["games_played"]

    # 4. Optional metadata merge + cleaning
    if include_team_meta:
        try:
            meta = nfl.import_team_desc()

            # Merge on appropriate key
            if "team" in meta.columns:
                team_stats = team_stats.merge(meta, on="team", how="left")
            elif "team_abbr" in meta.columns:
                team_stats = team_stats.merge(meta, left_on="team", right_on="team_abbr", how="left")

            # Fields to remove
            remove_cols = [
                c for c in team_stats.columns
                if any(keyword in c.lower() for keyword in [
                    "logo", "wordmark", "color", "nick", "division"
                ])
            ]

            team_stats = team_stats.drop(columns=remove_cols, errors="ignore")

        except Exception:
            pass

    # Add season
    team_stats["season"] = year

    # Reorder
    cols = [
        "season", "team",
        "games_played", "wins", "losses", "ties",
        "points_for", "points_against", "point_diff",
        "ppg_for", "ppg_against"
    ]
    other_cols = [c for c in team_stats.columns if c not in cols]

    return team_stats[cols + other_cols]


#df = get_team_season_data(2024)
#print(df.head)

def get_all_team_game_stats(year: int) -> pd.DataFrame:
    """
    Return game-by-game stats for every team in a given NFL season.
    One row per *team-game* (so each actual game appears twice: once per team).

    Columns include:
        - season, week, game_id, gameday
        - team, opponent, is_home
        - points_for, points_against, point_diff
        - result ('W', 'L', 'T')
    Compatible with nfl_data_py 0.3.3.
    """

    # 1. Load schedule data
    games = nfl.import_schedules([year])

    # Filter to regular season if column exists
    if "season_type" in games.columns:
        games = games[games["season_type"] == "REG"]

    # Drop games without final scores
    games = games.dropna(subset=["home_score", "away_score"])

    # 2. Build home team rows
    home = games.copy()
    home["team"] = home["home_team"]
    home["opponent"] = home["away_team"]
    home["is_home"] = True
    home["points_for"] = home["home_score"]
    home["points_against"] = home["away_score"]

    # 3. Build away team rows
    away = games.copy()
    away["team"] = away["away_team"]
    away["opponent"] = away["home_team"]
    away["is_home"] = False
    away["points_for"] = away["away_score"]
    away["points_against"] = away["home_score"]

    # 4. Combine into team-game logs
    team_games = pd.concat([home, away], ignore_index=True)

    # 5. Derived stats
    team_games["point_diff"] = team_games["points_for"] - team_games["points_against"]
    team_games["result"] = np.where(
        team_games["points_for"] > team_games["points_against"], "W",
        np.where(team_games["points_for"] < team_games["points_against"], "L", "T")
    )

    # 6. Keep / rename main columns (and keep extras if present)
    base_cols = [
        "season" if "season" in team_games.columns else None,
        "week" if "week" in team_games.columns else None,
        "gameday" if "gameday" in team_games.columns else None,
        "game_id" if "game_id" in team_games.columns else None,
        "team", "opponent", "is_home",
        "points_for", "points_against", "point_diff", "result",
    ]
    base_cols = [c for c in base_cols if c is not None]

    # Put base columns first, then everything else
    other_cols = [c for c in team_games.columns if c not in base_cols]
    team_games = team_games[base_cols + other_cols]

    # Sort by team + week if week exists
    if "week" in team_games.columns:
        team_games = team_games.sort_values(["team", "week"]).reset_index(drop=True)

    return team_games

def get_team_game_stats(year: int, team: str) -> pd.DataFrame:
    """
    Get game-by-game stats for a single team in a given season.

    Args:
        year (int): NFL season (e.g., 2024)
        team (str): Team abbreviation, e.g. 'PHI', 'DAL', 'KC'

    Returns:
        pandas.DataFrame: one row per game for that team.
    """
    team = team.upper()
    all_games = get_all_team_game_stats(year)
    return all_games[all_games["team"] == team].reset_index(drop=True)

phi_2024 = get_team_game_stats(2024, "PHI")
print(phi_2024[["week", "team", "opponent", "is_home", "points_for", "points_against", "result"]])


def get_team_touchdown_stats(year: int) -> pd.DataFrame:
    """
    Build touchdown stats for each team using play-by-play data.
    Compatible with nfl_data_py 0.3.3.
    """

    pbp = nfl.import_pbp_data([year])

    # Determine scoring team (posteam for offensive TDs, defteam for defensive TDs)
    pbp["team"] = pbp["posteam"].fillna(pbp["defteam"])

    # Create TD type indicators
    pbp["rush_td"] = pbp.get("rush_touchdown", 0)
    pbp["pass_td"] = pbp.get("pass_touchdown", 0)

    # Defensive TD (fumble return, interception return)
    pbp["def_td"] = pbp.get("defensive_touchdown", 0)

    # Special teams TD (punt return, kickoff return, blocked FG return)
    pbp["special_td"] = pbp.get("special_teams_touchdown", 0)

    # Total touchdowns
    pbp["total_td"] = (
        pbp["rush_td"] +
        pbp["pass_td"] +
        pbp["def_td"] +
        pbp["special_td"]
    )

    # Group by team
    td_stats = pbp.groupby("team").agg(
        total_td=("total_td", "sum"),
        rush_td=("rush_td", "sum"),
        pass_td=("pass_td", "sum"),
        def_td=("def_td", "sum"),
        special_td=("special_td", "sum"),
    ).reset_index()

    return td_stats

def get_team_season_with_tds(year: int) -> pd.DataFrame:
    base_df = get_team_season_data(year)
    td_df = get_team_touchdown_stats(year)

    merged = base_df.merge(td_df, on="team", how="left")

    td_cols = ["total_td", "rush_td", "pass_td", "def_td", "special_td"]
    for col in td_cols:
        merged[col] = merged[col].fillna(0).astype(int)

    return merged


def plot_team_stat_bar(year: int, stat_col: str):
    df = get_team_season_with_tds(year)

    if stat_col not in df.columns:
        raise ValueError(f"Column '{stat_col}' not found. "
                         "Did you mean one of: points_for, rush_td, pass_td, total_td?")
    
    df = df.sort_values(stat_col, ascending=False)

    teams = df["team"]
    values = df[stat_col]

    plt.figure(figsize=(12, 6))
    plt.bar(teams, values)
    plt.title(f"{year} - Team Comparison by {stat_col.replace('_',' ').title()}")
    plt.xticks(rotation=45)
    plt.xlabel("Team")
    plt.ylabel(stat_col.replace("_"," ").title())
    plt.tight_layout()
    plt.show()

# plot_team_stat_bar(2024, "total_td")

# plot_team_stat_bar(2024, "total_td")
# plot_team_stat_bar(2022, "rush_td")
