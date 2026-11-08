"""Data wrangling functions for NBA analysis."""

import pandas as pd

from .database import read_sql_query


# --------------------------------------------------
# Insight 1: Evolution of NBA Scoring
# --------------------------------------------------

SCORING_QUERY = """
WITH regular_season_games AS (

    SELECT

        CAST(
            SUBSTR(CAST(season_id AS TEXT), 2, 4)
            AS INTEGER
        ) AS season_start_year,

        pts_home + pts_away AS total_points

    FROM game

    WHERE season_type = 'Regular Season'
      AND pts_home IS NOT NULL
      AND pts_away IS NOT NULL
)

SELECT

    season_start_year,

    printf(
        '%d-%02d',
        season_start_year,
        (season_start_year + 1) % 100
    ) AS season,

    COUNT(*) AS number_of_games,

    ROUND(
        AVG(total_points),
        2
    ) AS avg_total_points

FROM regular_season_games

GROUP BY season_start_year

ORDER BY season_start_year
"""


def get_scoring_trends() -> pd.DataFrame:
    """Calculate average total points per game by season."""

    return read_sql_query(SCORING_QUERY)


# --------------------------------------------------
# Insight 2: The Three-Point Revolution
# --------------------------------------------------

THREE_POINT_QUERY = """
WITH regular_season_games AS (

    SELECT

        CAST(
            SUBSTR(CAST(season_id AS TEXT), 2, 4)
            AS INTEGER
        ) AS season_start_year,

        fg3a_home + fg3a_away AS total_3pa,

        fga_home + fga_away AS total_fga

    FROM game

    WHERE season_type = 'Regular Season'

      AND CAST(
          SUBSTR(CAST(season_id AS TEXT), 2, 4)
          AS INTEGER
      ) >= ?

      AND fg3a_home IS NOT NULL
      AND fg3a_away IS NOT NULL
      AND fga_home IS NOT NULL
      AND fga_away IS NOT NULL
)

SELECT

    season_start_year,

    printf(
        '%d-%02d',
        season_start_year,
        (season_start_year + 1) % 100
    ) AS season,

    COUNT(*) AS number_of_games,

    ROUND(
        AVG(total_3pa),
        2
    ) AS avg_3pa_per_game,

    ROUND(
        SUM(total_3pa) * 100.0
        / NULLIF(SUM(total_fga), 0),
        2
    ) AS three_point_attempt_share

FROM regular_season_games

GROUP BY season_start_year

ORDER BY season_start_year
"""


def get_three_point_trends(
    start_year: int = 1985,
) -> pd.DataFrame:
    """Calculate three-point shooting trends by season."""

    return read_sql_query(
        THREE_POINT_QUERY,
        params=(start_year,),
    )


# --------------------------------------------------
# Data quality: Three-point statistics coverage
# --------------------------------------------------

THREE_POINT_COVERAGE_QUERY = """
SELECT

    CAST(
        SUBSTR(CAST(season_id AS TEXT), 2, 4)
        AS INTEGER
    ) AS season_start_year,

    COUNT(*) AS total_games,

    SUM(
        CASE
            WHEN fg3a_home IS NOT NULL
             AND fg3a_away IS NOT NULL
             AND fga_home IS NOT NULL
             AND fga_away IS NOT NULL
            THEN 1
            ELSE 0
        END
    ) AS games_with_stats,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN fg3a_home IS NOT NULL
                 AND fg3a_away IS NOT NULL
                 AND fga_home IS NOT NULL
                 AND fga_away IS NOT NULL
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS coverage_pct

FROM game

WHERE season_type = 'Regular Season'
  AND CAST(
      SUBSTR(CAST(season_id AS TEXT), 2, 4)
      AS INTEGER
  ) >= ?

GROUP BY season_start_year

ORDER BY season_start_year
"""


def get_three_point_coverage(
    start_year: int = 1979,
) -> pd.DataFrame:
    """Check the coverage of three-point shooting statistics."""

    return read_sql_query(
        THREE_POINT_COVERAGE_QUERY,
        params=(start_year,),
    )
