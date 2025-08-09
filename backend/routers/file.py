from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Request
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.databaseConfig import get_db
from aws.awsConfig import s3, sqs, S3_BUCKET_NAME, SQS_QUEUE_URL
from schemas.file import CurrFile
from models.file import File as FileModel
from models.chat import Chat
from utils.jwt import decode_jwt_token
import uuid
import uuid
import json

router = APIRouter(prefix="/file", tags=["File"])
# Allowed MIME types
ACCEPTED_MIME_TYPES = ["application/pdf", "image/png", "image/jpeg"]

@router.post("/upload")
async def upload(
    request: Request,
    uploaded_report: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        accessToken = request.cookies.get("accessToken")
        print(accessToken)
        if not accessToken:
            raise HTTPException(status_code=401, detail="Unauthenticated.")
        payload = decode_jwt_token(accessToken)
        user_id = payload["data"]["user_id"]

        # Checking if file of correct type is uploaded
        if uploaded_report.content_type not in ACCEPTED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Only PDFs, png, jpg or jpeg files are allowed")

        # Storing File to S3 Bucket
        file_name = f"{uuid.uuid4()}_{uploaded_report.filename}"
        s3.upload_fileobj(uploaded_report.file, S3_BUCKET_NAME, file_name)
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

        # Saving Stored file metadata to postgres
        # Temporarily hardcoidng user id
        report = FileModel(
            user_id = user_id,
            file_name = file_name,
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
            MessageBody = json.dumps(message)
        )

        return {
            "message": "File Uploaded Successfully!",
            "file_id": report.id,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/allFiles")
async def allFiles(
    request: Request,
    currFile: CurrFile,
    db: AsyncSession = Depends(get_db)
):
    try:
        accessToken = request.cookies.get("accessToken")
        print(accessToken)
        if not accessToken:
            raise HTTPException(status_code=401, detail="Unauthenticated.")
        payload = decode_jwt_token(accessToken)
        user_id = uuid.UUID(payload["data"]["user_id"])

        # Getting all the chats of the user
        chats_res = await db.execute(select(Chat).where(Chat.user_id == user_id, Chat.file_id != currFile.file_id))
        chats = chats_res.scalars().all()  
        result = []
        
        for chat in chats:
            result.append({
                "chat_id": chat.chat_id,
                "title": chat.title
            })
        
        return {
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))