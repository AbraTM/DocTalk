import os
import time
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_HASHING_ALGORITHM = os.getenv("JWT_HASHING_ALGORITHM")

def encode_jwt_token(data: dict, expires_in: int = 3000):
    token_data = data.copy()
    token_data["exp"] = int(time.time()) + expires_in
    jwt_token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_HASHING_ALGORITHM)
    return jwt_token

def decode_jwt_token(jwt_token: str):
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_HASHING_ALGORITHM])
        return {
            "status": "success",
            "data": payload
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "message": "Token has expired." 
        }
    except JWTError:
        return {
            "status": "error",
            "message": "Invalid Token." 
        }