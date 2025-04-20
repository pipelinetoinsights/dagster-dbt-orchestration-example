# chess_pipeline/assets.py

from dagster import AssetOut, Output, multi_asset, AssetExecutionContext, AssetKey
import sys
from pathlib import Path

# Ensure ingestion can be imported
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ingestion.extract import run_extract

@multi_asset(
    outs={
        "chess_raw_stats": AssetOut(
            key=AssetKey(["raw", "chess_raw_stats"]),
            group_name="raw_ingestion",
            is_required=False,
        ),
        "chess_raw_games": AssetOut(
            key=AssetKey(["raw", "chess_raw_games"]),
            group_name="raw_ingestion",
            is_required=False,
        ),
    },
    can_subset=True,
)
def raw_chess_data(context: AssetExecutionContext):
    context.log.info("Starting raw data extraction...")

    try:
        run_extract(limit=20)
        context.log.info("Extraction complete.")
    except Exception as e:
        raise Exception(f"Extract failed: {e}")

    # Return dummy values for Dagster tracking (real loading is done in `run_extract`)
    if "chess_raw_stats" in context.selected_output_names:
        yield Output(value=None, output_name="chess_raw_stats")
    if "chess_raw_games" in context.selected_output_names:
        yield Output(value=None, output_name="chess_raw_games")
