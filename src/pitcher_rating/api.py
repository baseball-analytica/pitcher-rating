from argparse import Namespace
from datetime import datetime
import time
from typing import Any

import pybaseball
import pandas as pd
import numpy as np


def print_season_pitchers(
    args: Namespace,
) -> None:
    """
    Print the result of `get_season_pitchers` to the console.
    """
    season = args.season
    ascending = args.ascending
    limit = args.limit
    output = args.output

    result = get_season_pitchers(
        season,
        ascending,
        limit
    )

    print(result)

    if output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"./.output/season_pitchers_{timestamp}.json"
        result.to_json(filepath, orient="records", indent=4)
        print(f"saved this result to {filepath}")
    

def get_season_pitchers(
    season: int,
    ascending: bool,
    limit: int = 20,
) -> pd.DataFrame:
    """
    Obtain pitcher ratings for all pitchers in the given season.
    """
    pitcher_data = pybaseball.pitching_stats(season)
    pitcher_data = calculate_pitcher_ratings(pitcher_data)
    pitcher_data = pitcher_data.sort_values(by="Rating", ascending=ascending)

    cols = ["Name", "Team", "IP", "SO", "BB", "HBP", "HR", "Rating"]
    pitcher_data = pitcher_data[cols]

    return pitcher_data.head(limit)


def print_season_teams(
    args: Namespace,
) -> None:
    """
    Print the results of `get_season_teams` to the console.
    """
    season = args.season
    ascending = args.ascending
    output = args.output

    result = get_season_teams(
        season,
        ascending
    )

    print(result)

    if output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"./.output/season_teams_{timestamp}.json"
        result.to_json(filepath, orient="records", indent=4)
        print(f"saved this result to {filepath}")


def get_season_teams(
    season: int,
    ascending: bool,
) -> pd.DataFrame:
    """
    Obtain pitcher ratings for all teams in the given season.
    """
    team_data = pybaseball.team_pitching(season)
    team_data = calculate_pitcher_ratings(team_data)
    team_data = team_data.sort_values(by="Rating", ascending=ascending)

    cols = ["Team", "IP", "SO", "BB", "HBP", "HR", "Rating"]
    team_data = team_data[cols]

    return team_data


def print_seasons(
    args: Namespace,
) -> None:
    """
    Print the results of `get_seasons` to the console.
    """
    start = args.start
    end = args.end
    output = args.output

    result = get_seasons(
        start,
        end
    )

    print(result)

    if output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"./.output/seasons_{timestamp}.json"
        result.to_json(filepath, orient="records", indent=4)
        print(f"saved this result to {filepath}")


def get_seasons(
    start: int,
    end: int,
) -> pd.DataFrame:
    """
    Obtain league-average pitcher ratings for the given range of seasons.
    """
    seasons_data = pybaseball.team_pitching(start, end)
    seasons = seasons_data["Season"].unique().tolist()

    season_rows: list[dict[str, Any]] = []

    for s in seasons:
        season_data = seasons_data[seasons_data["Season"] == s]

        row: dict[str, Any] = {}

        row["Season"] = int(s)
        row["SO"] = season_data["SO"].sum().astype(int)
        row["BB"] = season_data["BB"].sum().astype(int)
        row["HBP"] = season_data["HBP"].sum().astype(int)
        row["HR"] = season_data["HR"].sum().astype(int)
        row["TBF"] = season_data["TBF"].sum().astype(int)
        row["K%"] = row["SO"] / row["TBF"]
        row["BB%"] = row["BB"] / row["TBF"]

        season_rows.append(row)

    result = pd.DataFrame(season_rows)
    result = calculate_pitcher_ratings(result)
    result = result.sort_values(by="Season", ascending=True)
    
    cols = ["Season", "SO", "BB", "HBP", "HR", "TBF", "Rating"]
    result = result[cols]

    return result


def calculate_pitcher_ratings(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append a column of pitcher ratings to this DataFrame.
    """
    a = (df["K%"] - 0.1) * 8 # strikeout term
    b = 2.375 - (df["BB%"] * 12) # walk term
    c = 2.375 - (df["HBP"] / df["TBF"] * 12) # HBP term
    d = 2.375 - (df["HR"] / df["TBF"] * 52) # home run term

    a = _clamp(a)
    b = _clamp(b)
    c = _clamp(c)
    d = _clamp(d)

    ratings = (a + b + c + d) / 6 * 100
    df["Rating"] = ratings

    return df


def _clamp(
    s: pd.Series,
    min: float = 0.0,
    max: float = 2.375,
) -> pd.Series:
    """
    Set all values above the max to max, and all values below the min to the min.
    """
    s = s.apply(lambda x: min if x < min else x)
    s = s.apply(lambda x: max if x > max else x)

    return s