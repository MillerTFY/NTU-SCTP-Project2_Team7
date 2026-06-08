# definitions.py
# Pattern: Lesson 2.6 definitions.py structure
#          + Lesson 2.7 Extra II PipesSubprocessClient resource

from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
    PipesSubprocessClient,    # from lesson 2.7 Extra II
)
# Change this line to import your assets module
#from . import assets
# To this if it still errors
from listenbrainz_dagster import assets

# ── Load all assets from assets.py ────────────────────────
# Pattern: lesson 2.6 definitions.py
all_assets = load_assets_from_modules([assets])

# ── Define jobs ───────────────────────────────────────────
# Full pipeline: snapshot → run → test
listenbrainz_pipeline_job = define_asset_job(
    name="listenbrainz_pipeline_job",
    selection=AssetSelection.all(),
    description="Full ListenBrainz ELT: dbt snapshot → dbt run → dbt test"
)

# ── Define schedules ──────────────────────────────────────
# Pattern: lesson 2.6 ScheduleDefinition inline in definitions.py
weekly_pipeline_schedule = ScheduleDefinition(
    name="weekly_pipeline_schedule",
    job=listenbrainz_pipeline_job,
    cron_schedule="0 0 * * 0",   # Every Sunday midnight
)

daily_test_schedule = ScheduleDefinition(
    name="daily_test_schedule",
    job=define_asset_job(
        name="daily_quality_job",
        selection=AssetSelection.assets("dbt_test"),
    ),
    cron_schedule="0 6 * * *",   # Every day 6am
)

# ── Definitions object ────────────────────────────────────
# Pattern: lesson 2.6 Definitions combining assets + jobs
#          + lesson 2.7 Extra II resources
defs = Definitions(
    assets=all_assets,
    jobs=[listenbrainz_pipeline_job],
    schedules=[weekly_pipeline_schedule, daily_test_schedule],
    resources={
        "pipes_subprocess_client": PipesSubprocessClient(),
    },
)
