from fastapi import APIRouter, Depends, HTTPException, Header, Response
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
        secure=False,
        samesite="lax"
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
    print(user_data)
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










# # Helper Function to set JWT token to a HttpOnly Cookie
# # JWT cookie for 7 days
# async def set_jwt_cookie(response: Response, user_id: str):
#     id_jwt_token = encode_jwt_token({
#         "user_id": str(user_id)
#     }, 60 * 60  * 24 * 7)
#     response.set_cookie(
#         key="token",
#         value=id_jwt_token,
#         httponly=True,
#         secure=True,
#         samesite="lax"
#     )

# @router.post("/create")
# async def createUser(
#     user_data: UserCreate,
#     response: Response,
#     db: AsyncSession = Depends(get_db),
# ) -> UserOut:
#         # First Checking if user already exists
#         user_res = await db.execute(select(User).where(User.email == user_data.email))
#         existing_user = user_res.scalar_one_or_none()
#         if existing_user:
#             raise HTTPException(status_code=400, detail="User already exists.")
        
#         new_user = User(**user_data.model_dump())
#         db.add(new_user)
#         await db.commit()
#         await db.refresh(new_user)
#         await set_jwt_cookie(response, new_user.id)
#         return new_user


# @router.post("/login")
# async def signin(
#     user_data: UserLogin,
#     response: Response,
#     db: AsyncSession = Depends(get_db)
# ) -> UserOut:
#     user_res = await db.execute(select(User).where(User.email == user_data.email))
#     existing_user = user_res.scalar_one_or_none()

#     # Validating that the users exists to login
#     if not existing_user:
#         raise HTTPException(status_code=401, detail="No user with this email.")

#     # Checking password if the user was an email-pass auth signed up
#     if not verify_password(user_data.password, existing_user.password):
#         raise HTTPException(status_code=401, detail="Invalid Credentials.")
        
#     await set_jwt_cookie(response, existing_user.id)
#     return existing_user

# @router.post("/firebase")
# async def firebaseAuth(
#     response: Response,
#     authorization: str = Header(...),
#     db: AsyncSession = Depends(get_db)
# ):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing Firebase token.")
    
#     fb_token = authorization.split(" ")[1]
#     user = get_user_info(fb_token)

#     user_res = await db.execute(select(User).where(User.fb_id == user["uid"]))
#     existing_user = user_res.scalar_one_or_none()
#     if existing_user:
#         await set_jwt_cookie(response, existing_user.id)
#         return existing_user
#     else:
#         user_res = await db.execute(select(User).where(User.email == user.email))
#         existing_user = user_res.scalar_one_or_none()
#         if existing_user:
#             raise HTTPException(status_code=400, detail="An account with this email already exists. Please log in with your password.")
#     user_name = user["name"].split(" ")
#     new_user = User(
#         first_name = user_name[0],
#         last_name = user_name[1] if len(user_name) > 1 else "",
#         email = user.email
#     )
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#     await set_jwt_cookie(response, new_user.id)
#     return new_user


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