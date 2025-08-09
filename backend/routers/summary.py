from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.summary import SummaryCreate
from schemas.file import CurrFile
from models.file import File
from models.summary import Summary
from db.databaseConfig import get_db
from utils.jwt import decode_jwt_token
from utils.get_s3_key import get_s3_key
from aws.awsConfig import s3, S3_BUCKET_NAME
import os
import json

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.post("/save")
async def saveSummary(
    summary_info: SummaryCreate,
    db: AsyncSession = Depends(get_db)
):
    file_id = summary_info.file_id
    result = await db.execute(select(File).where(File.id == file_id))
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=400, detail="Invalid File ID.")
    
    summary = Summary(
        file_id = summary_info.file_id,
        summary_s3_url = summary_info.summary_s3_url
    )
    db.add(summary)
    await db.commit()
    await db.refresh(summary)

    return {
        "message": "Summary info successfully stored"
    }


TEMP_FOLDER = "temp"
os.makedirs("temp", exist_ok=True)
@router.post("/getSummary")
async def getSummary(
    request: Request,
    currFile: CurrFile,
    db: AsyncSession = Depends(get_db)
):
    try:
        print(currFile.file_id)
        accessToken = request.cookies.get("accessToken")
        if not accessToken:
            raise HTTPException(status_code=401, detail="Missing Access token.")
        payload = decode_jwt_token(accessToken)
        user_id = payload["data"]["user_id"]

        # Add Code to check if the current user is the one that uploaded this file, for security

        # Getting the summary
        summary_res = await db.execute(select(Summary).where(Summary.file_id == currFile.file_id))
        summary_info = summary_res.scalar_one_or_none()
        if not summary_info:
            return {
                "status": "processing",
                "summary": None
            }

        # Getting the json summary from s3
        summary_s3_key = get_s3_key(summary_info.summary_s3_url)
        summary_obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=summary_s3_key)
        json_bytes = summary_obj['Body'].read()
        summary = json.loads(json_bytes.decode('utf-8'))
        return{
            "status": "ready",
            "data": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



