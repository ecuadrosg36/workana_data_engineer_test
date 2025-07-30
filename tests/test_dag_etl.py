import os

# Fix para entorno CI: usar /tmp para AIRFLOW_HOME
os.environ["AIRFLOW_HOME"] = "/tmp/airflow"
os.makedirs("/tmp/airflow", exist_ok=True)

from airflow.models import DagBag

def test_dag_import():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    
    # Si hubo errores de importación, mostrarlos
    assert dag_bag.import_errors == {}, f"Errores de importación: {dag_bag.import_errors}"
    
    dag = dag_bag.get_dag("etl_transactions_dag")
    assert dag is not None, "El DAG no fue encontrado o tiene errores de importación"
    assert len(dag.tasks) >= 1, "El DAG debería tener al menos una tarea"
