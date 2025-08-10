import json
import uuid
import google.generativeai as genai
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import update, func, select
from db.databaseConfig import get_db_session_context
from aws.awsConfig import s3, S3_BUCKET_NAME
from models.user import User
from models.chat import Chat
from models.file import File
from models.summary import Summary
from models.message import Message, Role
from utils.get_s3_key import get_s3_key
from utils.jwt import decode_jwt_token
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
router = APIRouter(prefix="/ws", tags=["Chat"])

@router.websocket("/chat")
async def chat_socket(
    websocket: WebSocket,
    fileId: str,
    token: str
):
    await websocket.accept()
    decoded_token = decode_jwt_token(token)
    if decoded_token.get("status") != "success":
        await websocket.close(code=4001, reason=decoded_token.get("message", "Something went wrong"))
        return
    
    try:
        user_id = uuid.UUID(decoded_token["data"]["user_id"])
    except Exception as e:
        print("Invalid user_id in token:", decoded_token.get("data"))
        await websocket.close(code=4002, reason="Invalid token payload")
        return
    try:
        file_id_uuid = uuid.UUID(fileId)
    except Exception as e:
        print("Invalid fileId provided:", fileId)
        await websocket.close(code=4003, reason="Invalid file id")
        return

    async with get_db_session_context() as db:
        try:
            # Checking if the user is a valid user
            user_result = await db.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()
            if not user:
                await websocket.close(code=4000, reason="User doesn't exist.")
                return
            
            # Checking if current user is the one that uploaded this file
            file_result = await db.execute(select(File).where(File.id == file_id_uuid, File.user_id == user_id))
            if not file_result.scalar_one_or_none():
                await websocket.close(code=4001, reason="This file wasn't uploaded by the current.")
                return
            
            # With the summary_id as a search param retrieving the summary file
            summary_result = await db.execute(select(Summary).where(Summary.file_id == file_id_uuid))
            summary = summary_result.scalar_one_or_none()
            if not summary:
                await websocket.close(code=4002, reason="No summary with the provided id.")
                return
            summary_s3_url = summary.summary_s3_url
            s3_key = get_s3_key(summary_s3_url)

            # Retreving the summary data from s3 bucket
            summary_obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
            json_bytes = summary_obj['Body'].read()
            summary_data = json.loads(json_bytes.decode('utf-8'))

            # Initialzing Chat and Chat History
            # Checking if a chat with this file already exists
            chat_result = await db.execute(select(Chat).where(Chat.file_id == file_id_uuid))
            chat = chat_result.scalar_one_or_none()
            chat_history = []

            if chat:
                messages_result = await db.execute(
                    select(Message).where(Message.chat_id == chat.chat_id).order_by(Message.created_at.asc(), Message.message_id.asc())
                )
                messages = messages_result.scalars().all()
                for msg in messages:
                    role_str = msg.role.value if hasattr(msg.role, "value") else str(msg.role)
                    chat_history.append({
                        "role": role_str,
                        "parts": [msg.content]
                    })
            else:
                # For the particular user created a new chat
                title_content = summary_data["main_finding"]
                words = title_content.split()
                title_display = " ".join(words[:6])
                if len(words) > 6:
                    title_display += "..."

                new_chat = Chat(
                    user_id = user.id,
                    file_id = fileId,
                    title = title_display
                )
                db.add(new_chat)
                await db.commit()
                await db.refresh(new_chat)
                chat = new_chat
            
            # Now intializing the LLM
            system_prompt = f"""
                You are a medical assitant, trying to help a non-professional patient with the queries
                based on the summary of their medical report and also the previously asked questions.
                
                SUMMARY:
                {json.dumps(summary_data, indent=2)}
            """
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_prompt)
            convo = model.start_chat(history=chat_history)

            while True:
                user_msg = await websocket.receive_text()
                response = convo.send_message(user_msg)
                assistant_msg = response.text

                # Sending message to frontend
                try:
                    await websocket.send_text(assistant_msg)
                except WebSocketDisconnect:
                    break

                now = datetime.now(timezone.utc)
                # Saving the user's msg and the assistant's response to db
                db.add(Message(
                    chat_id = chat.chat_id,
                    role = Role.user,
                    content = user_msg,
                    created_at=now
                ))
                db.add(Message(
                    chat_id = chat.chat_id,
                    role = Role.assistant,
                    content = assistant_msg,
                    created_at=now
                ))
                await db.commit()

                # Updating the chat
                await db.execute(
                    update(Chat).where(Chat.chat_id == chat.chat_id).values(updated_at=func.now())
                )
                await db.commit()

        except WebSocketDisconnect:
            print(f"Client {websocket.client} disconnected.")
        except Exception as e:
            print(f"An unexpected error occurred in websocket: {e}")
            await websocket.close(code=4500, reason=f"Something went wrong, please try again later.")
    