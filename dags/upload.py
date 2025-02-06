import os
import boto3

def upload_to_s3(**context):
    # Get the file name returned from extract task using XCom
    ti = context['ti']
    csv_file = ti.xcom_pull(task_ids='extract_and_save_task')
    if not csv_file:
        raise ValueError("No CSV file was returned from extract task!")

    # Get AWS S3 settings from environment variables
    BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION")

    # Initialize boto3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region
    )

    # Upload file to S3; the key in S3 will be the same as the local filename
    try:
        s3_client.upload_file(csv_file, BUCKET_NAME, csv_file)
        print(f"Uploaded {csv_file} to S3 bucket {BUCKET_NAME}")
    except Exception as e:
        print(f"Failed to upload {csv_file} to S3: {e}")
        raise
