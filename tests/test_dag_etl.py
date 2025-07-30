from airflow.models import DagBag

def test_dag_import():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    assert dag_bag.import_errors == {}, f"Errores de importación: {dag_bag.import_errors}"
    assert "etl_transactions_dag" in dag_bag.dags, "etl_transactions_dag no fue encontrado"
