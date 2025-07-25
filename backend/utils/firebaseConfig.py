import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os

load_dotenv()
cred_path = os.getenv("FIREBASE_SDK_PATH")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
