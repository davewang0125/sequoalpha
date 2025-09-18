# AWS S3 Setup Guide

## 1. Create AWS S3 Bucket

1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/)
2. Click "Create bucket"
3. Choose a unique bucket name (e.g., `sequoalpha-documents-2024`)
4. Select region (e.g., `us-east-1`)
5. Keep default settings for now
6. Click "Create bucket"

## 2. Create IAM User for S3 Access

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click "Users" → "Create user"
3. Username: `sequoalpha-s3-user`
4. Select "Programmatic access"
5. Click "Next"

### 3. Attach S3 Policy

1. Click "Attach policies directly"
2. Search for "S3" and select "AmazonS3FullAccess"
3. Click "Next" → "Create user"

### 4. Get Access Keys

1. Click on the created user
2. Go to "Security credentials" tab
3. Click "Create access key"
4. Select "Application running outside AWS"
5. Click "Create access key"
6. **IMPORTANT**: Copy and save both:
   - Access Key ID
   - Secret Access Key

## 5. Configure Environment Variables

Add these to your Render environment variables:

```
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket-name
```

## 6. Test Configuration

The backend will automatically:
- Upload files to S3 when uploaded
- Generate presigned URLs for downloads
- Fall back to local storage if S3 fails

## 7. Benefits

- ✅ Files persist even when server restarts
- ✅ No more 404 errors
- ✅ Better performance
- ✅ Scalable storage
- ✅ Direct download URLs
