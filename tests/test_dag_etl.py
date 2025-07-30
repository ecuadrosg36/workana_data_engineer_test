from airflow.models import DagBag

def test_dag_import():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)

    assert dag_bag.import_errors == {}, f"Errores de importación: {dag_bag.import_errors}"

    dag = dag_bag.get_dag("etl_transactions_dag")
    assert dag is not None, "El DAG no fue encontrado o tiene errores de importación"
    assert len(dag.tasks) >= 2, "El DAG debe tener al menos 2 tareas"
