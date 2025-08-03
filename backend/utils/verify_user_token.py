from firebase_admin import auth
from fastapi import HTTPException

def verify_firebase_token(token: str) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Missing token.")
    
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token.")

def get_user_info(token: str) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Missing Firebase token.")
    try:
        decoded_token = auth.verify_id_token(token)
        user_info = auth.get_user(decoded_token["uid"])
        user_name = user_info.display_name.split(" ")
        user = {
            "fb_id": user_info.uid,
            "first_name": user_name[0],
            "last_name": user_name[1] if len(user_name) > 1 else "",
            "email": user_info.email,
        }
        return user
    except Exception as e:
        print(f"Firebase verification error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token lalas.")