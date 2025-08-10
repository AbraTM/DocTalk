from fastapi import APIRouter, Request, Depends, HTTPException
from models.chat import Chat
from models.message import Message
from schemas.file import CurrFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.databaseConfig import get_db
from utils.jwt import decode_jwt_token
import uuid

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/")
async def getMessages(
    request: Request,
    currFile: CurrFile,
    db: AsyncSession = Depends(get_db)
):
    try:
        accessToken = request.cookies.get("accessToken")
        if not accessToken:
            raise HTTPException(status_code=401, detail="Unauthenticated.")
        payload = decode_jwt_token(accessToken)
        user_id = uuid.UUID(payload["data"]["user_id"])

        # Getting the current chat
        chats_res = await db.execute(select(Chat).where(Chat.user_id == user_id, Chat.file_id == currFile.file_id))
        chat = chats_res.scalar_one_or_none()
        if not chat:
            return {"messages": []} 
        
        # Getting all the messages from current chat
        messages_res = await db.execute(select(Message).where(Message.chat_id == chat.chat_id).order_by(Message.created_at.asc()))
        messages_data = messages_res.scalars().all()
        messages = []
        for msg in messages_data:
            messages.append({
                "sender": msg.role.value,
                "text": msg.content
            })
        
        print(messages)
        return {
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))