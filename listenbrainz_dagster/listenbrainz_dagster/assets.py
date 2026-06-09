# assets.py
# Pattern: Lesson 2.7 Extra II — PipesSubprocessClient
# Each dbt command = one Dagster asset
# Assets depend on each other via deps=[] parameter

from dagster import asset, AssetExecutionContext, PipesSubprocessClient

DBT_PROJECT_DIR = "/home/mille/NTU2026/NTU-SCTP-Project2_Team7/listenbrainz_Tables_demo"


# ── Asset 1: dbt snapshot ──────────────────────────────────
# Runs SCD Type 2 snapshot for dim_track
# No dependencies — runs first
@asset
def dbt_snapshot(
    context: AssetExecutionContext,
    pipes_subprocess_client: PipesSubprocessClient
):
    """
    Runs dbt snapshot to capture SCD Type 2 changes
    for dim_track (track_snapshot).
    """
    return pipes_subprocess_client.run(
        command=["dbt", "snapshot", "--no-partial-parse"],
        context=context,
        cwd=DBT_PROJECT_DIR
    ).get_results()


# ── Asset 2: dbt run ───────────────────────────────────────
# Builds all 8 models: staging → dimensions → fact → metrics
# Depends on dbt_snapshot completing first
@asset(deps=[dbt_snapshot])
def dbt_run(
    context: AssetExecutionContext,
    pipes_subprocess_client: PipesSubprocessClient
):
    """
    Runs all dbt models in order:
    - listenbrainz_dwh_staging.stg_listens
    - listenbrainz_dwh_star.dim_* (5 dimensions)
    - listenbrainz_dwh.fact_listens
    - listenbrainz_dwh_star.fct_user_metrics
    """
    return pipes_subprocess_client.run(
        command=["dbt", "run", "--no-partial-parse"],
        context=context,
        cwd=DBT_PROJECT_DIR
    ).get_results()


# ── Asset 3: dbt test ──────────────────────────────────────
# Runs all 39 tests: dbt core + dbt_utils + dbt_expectations
# Depends on dbt_run completing first
@asset(deps=[dbt_run])
def dbt_test(
    context: AssetExecutionContext,
    pipes_subprocess_client: PipesSubprocessClient
):
    """
    Runs 39 data quality tests:
    - dbt core: not_null, unique, relationships
    - dbt_utils: expression_is_true, accepted_range
    - dbt_expectations: row count, column ranges, value sets
    Expected: PASS=38 WARN=1 ERROR=0
    """
    return pipes_subprocess_client.run(
        command=["dbt", "test", "--no-partial-parse"],
        context=context,
        cwd=DBT_PROJECT_DIR
    ).get_results()