
from dagster import define_asset_job, ScheduleDefinition

weekly_project_job = define_asset_job(
    name="weekly_project_job",
    selection="*",
)

weekly_project_schedule = ScheduleDefinition(
    job=weekly_project_job,
    cron_schedule="0 2 * * 0",  # every Sunday at 2am
)