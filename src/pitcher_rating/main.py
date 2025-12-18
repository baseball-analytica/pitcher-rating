import argparse
import logging

from pybaseball import cache # type: ignore

from . import api
from .logger import init_logger


def main() -> None:
    cache.enable()

    parser = argparse.ArgumentParser(
        description="calculate pitcher ratings for MLB pitchers",
        epilog="report any bugs to akline at baseball-analytica dot com"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable logging"
    )
    subparser = parser.add_subparsers()

    pitchers_p = subparser.add_parser(
        "pitchers",
        help="obtain pitcher ratings for all pitchers in the given season",
        epilog=parser.epilog
    )
    pitchers_p.add_argument(
        "season",
        type=int,
        help="the year of the MLB season"
    )
    pitchers_p.add_argument(
        "-t",
        "--through",
        type=int,
        required=False,
        help="include all data through this season"
    )
    pitchers_p.add_argument(
        "-q",
        "--min-pa",
        type=float,
        required=False,
        help="specify a minimum number of plate appearances for each pitcher-season (default = qualified)"
    )
    pitchers_p.add_argument(
        "-a",
        "--ascending",
        action="store_true",
        help="order the data from lowest to highest rating"
    )
    pitchers_p.add_argument(
        "-l",
        "--limit",
        type=int,
        default=20,
        help="the number of pitcher-seasons to include"
    )
    pitchers_p.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="save the resulting data to a file"
    )
    pitchers_p.add_argument(
        "-c",
        "--chart",
        action="store_true",
        help="generate a matplotlib figure and save to a file"
    )
    pitchers_p.set_defaults(func=api.print_season_pitchers)

    teams_p = subparser.add_parser(
        "teams",
        help="obtain pitcher ratings for all teams in the given season",
        epilog=parser.epilog
    )
    teams_p.add_argument(
        "season",
        type=int,
        help="the year of the MLB season"
    )
    teams_p.add_argument(
        "-t",
        "--through",
        type=int,
        required=False,
        help="include all data through this season"
    )
    teams_p.add_argument(
        "-a",
        "--ascending",
        action="store_true",
        help="order the data from lowest to highest rating"
    )
    teams_p.add_argument(
        "-l",
        "--limit",
        type=int,
        default=30,
        help="the number of team-seasons to include"
    )
    teams_p.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="save the resulting data to a file"
    )
    teams_p.add_argument(
        "-c",
        "--chart",
        action="store_true",
        help="generate a matplotlib figure and save to a file"
    )
    teams_p.set_defaults(func=api.print_season_teams)

    seasons_p = subparser.add_parser(
        "seasons",
        help="obtain league-average pitcher ratings in the given range of seasons",
        epilog=parser.epilog
    )
    seasons_p.add_argument(
        "start",
        type=int,
        help="the first season to include"
    )
    seasons_p.add_argument(
        "end",
        type=int,
        help="the last season to include"
    )
    seasons_p.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="save the resulting data to a file"
    )
    seasons_p.add_argument(
        "-c",
        "--chart",
        action="store_true",
        help="generate a matplotlib figure and save to a file"
    )
    seasons_p.set_defaults(func=api.print_seasons)

    try:
        args = parser.parse_args()

        log_level = logging.DEBUG if args.verbose else logging.CRITICAL
        init_logger(log_level)

        args.func(args)
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()