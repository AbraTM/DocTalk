from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db.databaseConfig import get_db
from aws.awsConfig import s3, sqs, S3_BUCKET_NAME, SQS_QUEUE_URL
from models.file import File as FileModel
import uuid
import os

router = APIRouter(prefix="/file", tags=["File"])

TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload(
    uploaded_report: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Storing File to S3 Bucket
        file_name = f"{uuid.uuid4()}_{uploaded_report.filename}"
        s3.upload_fileobj(uploaded_report.file, S3_BUCKET_NAME, file_name)
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

        # Saving Stored file metadata to postgres
        # Temporarily hardcoidng user id
        user_id_hardcoded = "9ad2d375-0b32-43b2-951f-9ccbddde2eb8"
        report = FileModel(
            user_id = user_id_hardcoded,
            file_name = uploaded_report.filename,
            s3_url = s3_url
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)

        # Sending a message to SQS queue that a file has been uploaded
        # Process it when EC2 is available
        message = {
            "file_id": str(report.id),
            "file_name": report.file_name,
            "s3_url": report.s3_url
        }
        sqs.send_message(
            QueueUrl = SQS_QUEUE_URL,
            MessageBody = str(message)
        )

        return {
            "message": "File Uploaded Successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))