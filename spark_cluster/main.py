import boto3
from dotenv import load_dotenv
import os
load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET=os.getenv("AWS_S3_BUCKET")
AWS_REGION=os.getenv("AWS_REGION")

file_name = "hee.jpg"
object_name = "Procopter.jpg"

def main():
    print("Hello World")
    s3_client = boto3.client(
        service_name = 's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    # response = s3_client.upload_file(file_name, AWS_S3_BUCKET, object_name)
    response = s3_client.download_file(AWS_S3_BUCKET, object_name, file_name)

if __name__ == "__main__":
    main()