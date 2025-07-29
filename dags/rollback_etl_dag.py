from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "enman",
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    dag_id="rollback_etl_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Rollback de transacciones del último mes",
    tags=["rollback", "etl"],
) as dag:

    rollback_sqlite = BashOperator(
        task_id="rollback_sqlite_db",
        bash_command="sqlite3 /opt/airflow/project/data/transactions.db < /opt/airflow/project/sql/rollback_last_month.sql",
    )

    rollback_sqlite
