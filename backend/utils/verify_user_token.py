from firebase_admin import auth
from fastapi import HTTPException

def verify_firebase_token(token: str) -> str:
    if not token:
        raise HTTPException(status_code=400, detail="Missing token.")
    
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token.")
