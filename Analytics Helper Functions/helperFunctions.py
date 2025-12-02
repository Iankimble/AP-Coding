import nfl_data_py as nfl
import pandas as pd
import matplotlib.pyplot as plt

def get_season_totals_by_position(year: int, position: str) -> pd.DataFrame:
    """
    Return full-season stats for all players at a given position.

    Args:
        year (int): NFL season (e.g., 2024)
        position (str): Player position (e.g., 'QB', 'RB', 'WR', 'TE')

    Returns:
        pandas.DataFrame: One row per player with season-total stats.
    """
    # Load weekly stats for the season
    weekly = nfl.import_weekly_data([year])

    # Normalize position input
    pos = position.upper()

    # Make sure the 'position' column exists
    if "position" not in weekly.columns:
        raise ValueError("Column 'position' not found in weekly data.")

    # Filter to the requested position
    pos_df = weekly[weekly["position"] == pos].copy()

    # If nothing found, let the user know
    if pos_df.empty:
        raise ValueError(f"No data found for position '{pos}' in season {year}.")

    # Grouping columns that identify a player
    group_cols = ["player_display_name", "player_id", "position", "recent_team"]

    # Keep only columns that exist
    group_cols = [c for c in group_cols if c in pos_df.columns]

    # Numeric columns to sum (yards, TDs, attempts, etc.)
    numeric_cols = pos_df.select_dtypes(include="number").columns.tolist()

    # Group by player and sum numeric stats across all weeks
    season_totals = (
        pos_df[group_cols + numeric_cols]
        .groupby(group_cols, as_index=False)[numeric_cols]
        .sum()
    )

    # Optional: sort by a key stat depending on position
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

import nfl_data_py as nfl
import pandas as pd

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


playerData= get_player_stats(2024, 'Lamar','Jackson')
print(playerData)

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

#plot_player_stat_by_week(
#    2004,
#    "Brian",
#    "Westbrook",
#    "rushing_yards",
#    save_path="brian_westbrook_2004_rushing_yards_by_week.png"
#)