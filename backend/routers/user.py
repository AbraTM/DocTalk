from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserLogin, UserOut
from models.user import User
from db.databaseConfig import get_db
from utils.verify_user_token import get_user_info
from utils.jwt import encode_jwt_token
from utils.pass_hashing import verify_password

router = APIRouter(prefix="/user", tags=["user"])

# Method to create JWT token for frontend to use in subsequent requests
async def create_id_jwt(response: Response, id: str):
    id_token = encode_jwt_token({"user_id": str(id)} , 60 * 40 * 24 * 7)
    response.set_cookie(
        key="accessToken",
        value=id_token,
        httponly=True,
        secure=True,
        samesite="none"
    )

@router.post("/signin")
async def SignIn(
    response: Response,
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing firebase token.")

    firebase_token = authorization.split(" ")[1]
    user_data = get_user_info(firebase_token)
    user_fb_id = str(user_data["fb_id"])
    user_res = await db.execute(select(User).where(User.fb_id == user_fb_id))
    user = user_res.scalar_one_or_none()
    if not user:
        new_user = User(**user_data)
        user = new_user
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await create_id_jwt(response, user.id)

    return user

@router.post("/verify")
async def verify(accessToken: str | None = Cookie(None)):
    print(accessToken)
    return { "msg": "ok" }

# @router.post("/get_chat_token")
# async def getChatToken(payload: TokenCreate):
#     if not payload.firebase_token:
#         raise HTTPException(status_code=401, detail="Missing Firebase Token.")
#     user_fb_id = verify_firebase_token(payload.firebase_token)
#     if not user_fb_id:
#         raise HTTPException(status_code=401, detail="Invalid Firebase token.")
#     jwt_token = encode_jwt_token({
#         "user_fb_id": user_fb_id,
#         "summary_id": payload.summary_id
#     })
#     return { "token": jwt_token }