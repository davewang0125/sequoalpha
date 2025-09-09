import boto3
import os
from botocore.exceptions import ClientError
from flask import current_app

class S3Manager:
    def __init__(self):
        # Check if AWS credentials are properly configured
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        
        if not all([aws_access_key, aws_secret_key, self.bucket_name]):
            print("⚠️ AWS S3 credentials not properly configured, S3 features disabled")
            self.s3_client = None
            return
            
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            print(f"✅ S3 client initialized for bucket: {self.bucket_name}")
        except Exception as e:
            print(f"❌ Failed to initialize S3 client: {e}")
            self.s3_client = None
    
    def upload_file(self, file_path, s3_key):
        """Upload a file to S3"""
        if not self.s3_client:
            print("❌ S3 client not available, skipping upload")
            return False
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False
    
    def download_file(self, s3_key, local_path):
        """Download a file from S3"""
        if not self.s3_client:
            print("❌ S3 client not available, skipping download")
            return False
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            return True
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            return False
    
    def generate_presigned_url(self, s3_key, expiration=3600):
        """Generate a presigned URL for direct download"""
        if not self.s3_client:
            print("❌ S3 client not available, cannot generate presigned URL")
            return None
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def delete_file(self, s3_key):
        """Delete a file from S3"""
        if not self.s3_client:
            print("❌ S3 client not available, skipping deletion")
            return False
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            return False
    
    def file_exists(self, s3_key):
        """Check if a file exists in S3"""
        if not self.s3_client:
            print("❌ S3 client not available, file check skipped")
            return False
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError:
            return False

# Global S3 manager instance
s3_manager = S3Manager()
