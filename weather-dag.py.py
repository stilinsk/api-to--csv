from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the default_args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 5),  # Replace with your actual start date
    'retries': 0,  # No retries, since we want it to succeed and stop after one run
    'retry_delay': timedelta(seconds=30),  # Delay between retries (won't retry since retries=0)
    'max_active_runs': 1,  # Ensures only one run happens at a time
}

# Define the DAG
dag = DAG(
    'weather_etl',
    default_args=default_args,
    description='ETL DAG for weather data',
    schedule_interval=None,  # Set to None for manual triggering
    catchup=False,  # Don't run missed intervals
)

# Define the task to run the ETL script
run_weather_etl = BashOperator(
    task_id='run_weather_etl',
    bash_command='cd /home/stilinski/airflow_project/api-to--csv && python main.py',
    execution_timeout=timedelta(minutes=2),  # Ensure the task runs within 1 minute
    dag=dag,
)

# Set the task execution order
run_weather_etl
