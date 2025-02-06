from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import boto3
from dotenv import load_dotenv
from extract import extract_and_save
from upload import upload_to_s3

# Load environment variables
load_dotenv()

# Reddit API credentials from .env
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 5),  # Adjust as needed
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    'extract_news',
    default_args=default_args,
    description='Extract tech news, save as CSV and upload to s3',
    schedule_interval='@daily',  # Runs daily
    catchup=False
)

# Define task
extract_task = PythonOperator(
    task_id='extract_and_save_task',
    python_callable=extract_and_save,
    dag=dag,
)


# Task 2: Upload CSV to S3
upload_task = PythonOperator(
    task_id='upload_to_s3_task',
    python_callable=upload_to_s3,
    provide_context=True,  # Needed for XCom and context access
    dag=dag,
)

# Set task dependencies
extract_task >> upload_task


