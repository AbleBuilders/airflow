from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

def on_success_dag(dict):
    print('On success dag.')
    print(dict)

def on_failure_dag(dict):
    print('On failure dag.')
    print(dict)

def on_success_task(dict):
    print('On success task.')
    print(dict)

def on_failure_task(dict):
    print('On failure task.')
    print(dict)

default_args = {
    'start_date': datetime.now(),
    'owner': 'Airflow',
    'retries':3,
    'retry_delay': timedelta(seconds=60),
    'emails': ['harshraj.rathore@gmail.com'],
    'email_on_retry':True,
    'email_on_failure':True,
    'on_success_callback':on_success_task,
    'on_failure_callback':on_failure_task
}

with DAG(dag_id='alert_dag', schedule_interval="0 0 * * *", 
    default_args=default_args, catchup=True, 
    dagrun_timeout=timedelta(seconds=80),
    on_failure_callback=on_failure_dag,
    on_success_callback=on_success_dag) as dag:
    
    # Task 1
    t1 = BashOperator(task_id='t1', bash_command="exit 1")
    
    # Task 2
    t2 = BashOperator(task_id='t2', bash_command="echo 'second task'")

    t1 >> t2