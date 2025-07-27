from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.summary import SummaryCreate
from models.file import File
from models.summary import Summary
from db.databaseConfig import get_db

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