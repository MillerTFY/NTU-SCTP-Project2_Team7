# visualisations/config.py
import os
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

GCP_PROJECT   = os.getenv("GCP_PROJECT", "project-7789-m2gba")
BQ_DATASET    = os.getenv("BQ_DATASET", "M2_GBA")
BQ_TABLE      = os.getenv("BQ_TABLE", "fact_listen_history")

def get_bq_client():
    """Returns an authenticated BigQuery client."""
    return bigquery.Client(project=GCP_PROJECT)

def query_model(sql: str) -> "pd.DataFrame":
    """Run a SQL query against BigQuery and return a DataFrame."""
    import pandas as pd
    client = get_bq_client()
    return client.query(sql).to_dataframe()