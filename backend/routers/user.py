from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserOut
from schemas.token import TokenCreate
from models.user import User
from firebase_admin import auth
from db.databaseConfig import get_db
from utils.verify_user_token import verify_firebase_token
from utils.jwt import encode_jwt_token

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create")
async def createUser(
    user_data: UserCreate,
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Firebase Token.")
    id_token = authorization.split(" ")[1]

    try:
        decode_token = auth.verify_id_token(id_token)
        firebase_uid = decode_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token.")
    
    result = await db.execute(select(User).where(User.fb_id == firebase_uid))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return existing_user
    

    new_user = User(**user_data.model_dump(), fb_id = firebase_uid)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/signin")
async def signin(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Firebase Token.")
    id_token = authorization.split(" ")[1]
    
    try:
        decode_token = auth.verify_id_token(id_token)
        firebase_uid = decode_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token.")
    
    result = await db.execute(select(User).where(User.fb_id == firebase_uid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exists.")
    
    return user
    
@router.post("/get_chat_token")
async def getChatToken(payload: TokenCreate):
    if not payload.firebase_token:
        raise HTTPException(status_code=401, detail="Missing Firebase Token.")
    user_fb_id = verify_firebase_token(payload.firebase_token)
    if not user_fb_id:
        raise HTTPException(status_code=401, detail="Invalid Firebase token.")
    jwt_token = encode_jwt_token({
        "user_fb_id": user_fb_id,
        "summary_id": payload.summary_id
    })
    return { "token": jwt_token }