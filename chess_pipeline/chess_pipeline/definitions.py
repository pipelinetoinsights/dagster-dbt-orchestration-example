from dagster import Definitions
from dagster_dbt import DbtCliResource

from .dbt_assets import dbt_assets_def
from .assets import raw_chess_data
from .schedules import weekly_project_job, weekly_project_schedule

from pathlib import Path

DBT_PROJECT_PATH = Path(__file__).joinpath("..", "..", "..", "dbt").resolve()
DBT_PROFILES_PATH = DBT_PROJECT_PATH


defs = Definitions(
    assets=[dbt_assets_def, raw_chess_data],
    jobs=[weekly_project_job],
    schedules=[weekly_project_schedule],
    resources={
        "dbt": DbtCliResource(
            project_dir=DBT_PROJECT_PATH, profiles_dir=DBT_PROFILES_PATH
        )
    },
)
