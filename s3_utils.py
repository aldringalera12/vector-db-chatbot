"""
AWS S3 utilities for storing and retrieving vector database
"""

import os
import shutil
import zipfile
import boto3
from pathlib import Path
from typing import Optional


class S3DatabaseManager:
    """Manages vector database storage in AWS S3"""
    
    def __init__(self):
        """Initialize S3 client with credentials from environment"""
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("AWS_S3_BUCKET")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.db_key = "vector_db.zip"
        
        # Initialize S3 client if credentials are provided
        if self.access_key and self.secret_key and self.bucket_name:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            self.enabled = True
            print("✅ S3 storage enabled")
        else:
            self.s3_client = None
            self.enabled = False
            print("⚠️  S3 storage disabled (credentials not provided)")
    
    def download_database(self, db_path: str = "./vector_db") -> bool:
        """Download vector database from S3"""
        if not self.enabled:
            print("⚠️  S3 storage disabled, skipping download")
            return False
        
        try:
            print(f"📥 Downloading database from S3...")
            
            # Download zip file
            zip_path = f"{db_path}.zip"
            self.s3_client.download_file(
                self.bucket_name,
                self.db_key,
                zip_path
            )
            print(f"✅ Downloaded {zip_path}")
            
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(db_path)
            print(f"✅ Extracted to {db_path}")
            
            # Remove zip file
            os.remove(zip_path)
            print(f"✅ Database restored from S3")
            return True
            
        except self.s3_client.exceptions.NoSuchKey:
            print("⚠️  Database not found in S3 (first deployment)")
            return False
        except Exception as e:
            print(f"❌ Error downloading database: {e}")
            return False
    
    def upload_database(self, db_path: str = "./vector_db") -> bool:
        """Upload vector database to S3"""
        if not self.enabled:
            print("⚠️  S3 storage disabled, skipping upload")
            return False
        
        try:
            if not os.path.exists(db_path):
                print(f"⚠️  Database path not found: {db_path}")
                return False
            
            print(f"📤 Uploading database to S3...")
            
            # Create zip file
            zip_path = f"{db_path}.zip"
            shutil.make_archive(db_path, 'zip', db_path)
            print(f"✅ Created {zip_path}")
            
            # Upload to S3
            self.s3_client.upload_file(
                zip_path,
                self.bucket_name,
                self.db_key
            )
            print(f"✅ Uploaded to S3")
            
            # Remove zip file
            os.remove(zip_path)
            print(f"✅ Database backed up to S3")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading database: {e}")
            return False


# Global S3 manager instance
s3_manager: Optional[S3DatabaseManager] = None


def get_s3_manager() -> S3DatabaseManager:
    """Get or create S3 manager instance"""
    global s3_manager
    if s3_manager is None:
        s3_manager = S3DatabaseManager()
    return s3_manager

