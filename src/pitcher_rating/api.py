import logging
from argparse import Namespace
from datetime import datetime
from typing import Any

import pybaseball # type: ignore
import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)


def print_season_pitchers(
    args: Namespace,
) -> None:
    """
    Print the result of `get_season_pitchers` to the console.
    """
    logger.debug("print_season_pitchers called")
    logger.debug("parsing args...")

    season = args.season
    through = args.through
    ascending = args.ascending
    limit = args.limit
    output = args.output

    result = get_season_pitchers(
        season,
        through,
        ascending,
        limit
    )

    logger.debug("successfully obtained season pitcher data")
    print(result)

    if output:
        logger.debug("output = True, attempting to save outfile...")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"./.output/season_pitchers_{timestamp}.json"
            result.to_json(filepath, orient="records", indent=4)
            print(f"saved this result to {filepath}")
        except Exception as e:
            logger.error(f"failed to save season pitcher results: {e}")
            raise Exception(f"failed to save season pitcher results: {e}")
    

def get_season_pitchers(
    season: int,
    through: int | None,
    ascending: bool,
    limit: int = 20,
) -> pd.DataFrame:
    """
    Obtain pitcher ratings for all pitchers in the given season.
    """
    logger.debug("get_season_pitchers called")
    logger.debug(f"args: season = {season}, through = {through}, ascending = {ascending}, limit = {limit}")

    try:
        pitcher_data = pybaseball.pitching_stats(season, through)
    except Exception as e:
        logger.error(f"failed to get pitching_stats from pybaseball: {e}")
        raise Exception(f"failed to get pitching_stats from pybaseball: {e}")
    
    try:
        pitcher_data = calculate_pitcher_ratings(pitcher_data)

        logger.debug("sorting and cleaning columns...")
        pitcher_data = pitcher_data.sort_values(by="Rating", ascending=ascending)
        cols = ["Name", "Season", "Team", "IP", "SO", "BB", "HBP", "HR", "Rating"]
        pitcher_data = pitcher_data[cols]

        return pitcher_data.head(limit)
    except Exception as e:
        logger.error(f"failed to calculate season pitcher data: {e}")
        raise Exception(f"failed to calculate season pitcher data: {e}")


def print_season_teams(
    args: Namespace,
) -> None:
    """
    Print the results of `get_season_teams` to the console.
    """
    logger.debug("print_season_pitchers called")
    logger.debug("parsing args...")

    season = args.season
    through = args.through
    ascending = args.ascending
    output = args.output

    result = get_season_teams(
        season,
        through,
        ascending
    )

    logger.debug("successfully obtained season team data")
    print(result)

    if output:
        logger.debug("output = True, attempting to save outfile...")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"./.output/season_teams_{timestamp}.json"
            result.to_json(filepath, orient="records", indent=4)
            print(f"saved this result to {filepath}")
        except Exception as e:
            logger.error(f"failed to save season team results: {e}")
            raise Exception(f"failed to save season team results: {e}")


def get_season_teams(
    season: int,
    through: int | None,
    ascending: bool,
    limit: int = 30,
) -> pd.DataFrame:
    """
    Obtain pitcher ratings for all teams in the given season.
    """
    logger.debug("get_season_teams called")
    logger.debug(f"args: season = {season}, through = {through}, ascending = {ascending}, limit = {limit}")

    try:
        team_data = pybaseball.team_pitching(season, through)
    except Exception as e:
        logger.error(f"failed to get team_pitching from pybaseball: {e}")
        raise Exception(f"failed to get team_pitching from pybaseball: {e}")
    
    try:
        team_data = calculate_pitcher_ratings(team_data)

        logger.debug("sorting and cleaning columns...")
        team_data = team_data.sort_values(by="Rating", ascending=ascending)
        cols = ["Team", "Season", "IP", "SO", "BB", "HBP", "HR", "Rating"]
        team_data = team_data[cols]

        return team_data.head(limit)
    except Exception as e:
        logger.error(f"failed to calculate season team data: {e}")
        raise Exception(f"failed to calculate season team data: {e}")

def print_seasons(
    args: Namespace,
) -> None:
    """
    Print the results of `get_seasons` to the console.
    """
    logger.debug("print_season called")
    logger.debug("parsing args...")

    start = args.start
    end = args.end
    output = args.output

    result = get_seasons(
        start,
        end
    )

    logger.debug("successfully obtained season data")
    print(result)

    if output:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"./.output/seasons_{timestamp}.json"
            result.to_json(filepath, orient="records", indent=4)
            print(f"saved this result to {filepath}")
        except Exception as e:
            logger.error(f"failed to save season results: {e}")
            raise Exception(f"failed to save season results: {e}")

def get_seasons(
    start: int,
    end: int,
) -> pd.DataFrame:
    """
    Obtain league-average pitcher ratings for the given range of seasons.
    """
    logger.debug("get_season_teams called")
    logger.debug(f"args: start = {start}, end = {end}")

    try:
        seasons_data = pybaseball.team_pitching(start, end)
    except Exception as e:
        logger.error(f"failed to get team_pitching from pybaseball: {e}")
        raise Exception(f"failed to get team_pitching from pybaseball: {e}")
    
    try:
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

    except Exception as e:
        logger.error(f"failed to filter season data: {e}")
        raise Exception(f"failed to filter season data: {e}")

    try:
        result = pd.DataFrame(season_rows)
        result = calculate_pitcher_ratings(result)

        result = result.sort_values(by="Season", ascending=True)
        cols = ["Season", "SO", "BB", "HBP", "HR", "TBF", "Rating"]
        result = result[cols]

        return result
    except Exception as e:
        logger.error(f"failed to calculate season data: {e}")
        raise Exception(f"failed to calculate season data: {e}")

def calculate_pitcher_ratings(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append a column of pitcher ratings to this DataFrame.
    """
    logger.debug("calculate_pitcher_ratings called")

    try:
        logger.debug("calculating a, b, c, d...")
        a = (df["K%"] - 0.1) * 8 # strikeout term
        b = 2.375 - (df["BB%"] * 12) # walk term
        c = 2.375 - (df["HBP"] / df["TBF"] * 12) # HBP term
        d = 2.375 - (df["HR"] / df["TBF"] * 52) # home run term

        logger.debug("clamping a, b, c, d...")
        a = _clamp(a)
        b = _clamp(b)
        c = _clamp(c)
        d = _clamp(d)

        logger.debug("appending final pitcher ratings to DataFrame...")
        ratings = (a + b + c + d) / 6 * 100
        df["Rating"] = ratings

        return df
    except Exception as e:
        logger.error(f"failed to calculate pitcher ratings: {e}")
        raise Exception(f"failed to calculate pitcher ratings: {e}")


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