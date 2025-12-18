import logging
import sys


def init_logger(
    log_level: int,
) -> None:
    """
    Initialize the logger.
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(".logs/pitcher_rating.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)

    logger.info("initialized logger for pitcher_rating")