from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import firebaseConfig

description = """
    DocTalk is a web platform that helps users understand their medical test results by generating easy-to-read 
    summaries and providing an AI-powered chatbot for personalized explanations. Users can securely upload medical 
    reports, and the system uses a powerful language model to break down complex terms into simple language—all 
    within a smooth, session-based experience powered by Firebase Auth, FastAPI, PostgreSQL, and AWS services.
"""

app = FastAPI(
    title="DocTalk Backend",
    description=description,
    version="1.0.0",
    contact={
        "name": "Send email to Tushar Malhan",
        "email": "tusharmalhan2564@gmail.com"
    }
)

origins = [
    "http://localhost:3000",
    "https://doctalk-lac.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "DocTalk Backend"}