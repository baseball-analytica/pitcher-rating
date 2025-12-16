import argparse

from pybaseball import cache

from . import api


def main() -> None:
    cache.enable()

    parser = argparse.ArgumentParser(
        description="calculate pitcher ratings for MLB pitchers",
        epilog="report any bugs to akline at baseball-analytica dot com"
    )
    subparser = parser.add_subparsers()

    pitchers_p = subparser.add_parser(
        "pitchers",
        help="obtain pitcher ratings for all pitchers in the given season"
    )
    pitchers_p.add_argument(
        "season",
        type=int,
        help="the year of the MLB season"
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
        help="the number of pitchers to include"
    )
    pitchers_p.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="save the resulting data to a file"
    )
    pitchers_p.set_defaults(func=api.print_season_pitchers)

    teams_p = subparser.add_parser(
        "teams",
        help="obtain pitcher ratings for all teams in the given season"
    )
    teams_p.add_argument(
        "season",
        type=int,
        help="the year of the MLB season"
    )
    teams_p.add_argument(
        "-a",
        "--ascending",
        action="store_true",
        help="order the data from lowest to highest rating"
    )
    teams_p.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="save the resulting data to a file"
    )
    teams_p.set_defaults(func=api.print_season_teams)

    seasons_p = subparser.add_parser(
        "seasons",
        help="obtain league-average pitcher ratings in the given range of seasons"
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
    seasons_p.set_defaults(func=api.print_seasons)


    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()