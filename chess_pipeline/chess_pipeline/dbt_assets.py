from pathlib import Path
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets, DagsterDbtTranslator
from typing import Mapping, Any, Optional

# Point to your dbt project and profiles directories
dbt_project = DbtProject(
    project_dir=Path(__file__).resolve().parents[2] / "dbt",
    profiles_dir=Path(__file__).resolve().parents[2] / "dbt",
)


class CustomTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        meta = dbt_resource_props.get("meta", {})
        dagster_meta = meta.get("dagster", {}) if isinstance(meta, dict) else {}

        return dagster_meta.get("layer", "dbt_models")


dbt_project.prepare_if_dev()


@dbt_assets(
    manifest=dbt_project.manifest_path, dagster_dbt_translator=CustomTranslator()
)
def dbt_assets_def(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
