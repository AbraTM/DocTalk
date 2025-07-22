# 🩺 DocTalk – Understand Your Medical Reports with AI

DocTalk is an AI-powered platform that helps non-professionals understand complex medical test reports. It generates human-readable summaries from uploaded documents (PDFs, images, text) and includes a conversational chatbot to answer health-related questions — making healthcare data truly accessible.

---

## 🚀 Features

- 🧠 **LLM-powered Summarization** – Converts complex lab reports into simple explanations using state-of-the-art language models (Gemini, OpenAI, etc.).
- 💬 **Interactive Chatbot** – Ask follow-up questions about your reports or conditions using a health-aware chatbot.
- 🖼️ **PDF/Image/Text Support** – Upload multiple formats for interpretation.
- ☁️ **AWS-Driven Asynchronous Processing** – Scalable background tasks using SQS, ECS, and S3.
- 🌐 **Modern Tech Stack** – Built with FastAPI, ReactJS, and containerized for deployment.

---

## 🧱 Tech Stack

| Layer             | Technology                    |
|------------------|-------------------------------|
| Frontend         | ReactJS, TailwindCSS          |
| Backend API      | FastAPI                       |
| LLM Integration  | Gemini Pro / OpenAI GPT       |
| Storage          | AWS S3                        |
| Async Tasks      | AWS SQS + ECS (Worker Service)|
| Auth (Planned)   | Cognito / JWT-based system    |
| Containerization | Docker + Docker Compose       |
| Deployment       | AWS (ECS / Fargate / ECR)     |

---

## 🗂️ Folder Structure (Planned)

/frontend -> ReactJS frontend (UI + chatbot)
/backend -> FastAPI server
└── /routes -> API routes (upload, chat, status)
└── /workers -> ECS/SQS workers
└── /services -> AWS S3/SQS integrations
└── /llm -> Summarization & chat logic
/model -> Preprocessing/LLM utilities
/docs -> Sample medical reports

yaml
Copy
Edit

---

## 🛠️ Setup Instructions
---

## 🗂️ Folder Structure (Planned)

```
/frontend        -> ReactJS frontend (UI + chatbot)
/backend         -> FastAPI server
  └── /routes     -> API routes (upload, chat, status)
  └── /workers    -> ECS/SQS workers
  └── /services   -> AWS S3/SQS integrations
  └── /llm        -> Summarization & chat logic
/model           -> Preprocessing/LLM utilities
/docs            -> Sample medical reports
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/DocTalk.git
cd DocTalk
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 4. Environment Variables (Example)

Create a `.env` file in the backend directory with the following:

```env
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
SQS_QUEUE_URL=your_sqs_url
S3_BUCKET_NAME=your_bucket_name
```

---

## 🧪 Sample Use Cases

- 📤 Upload your **CBC, LFT, or X-ray** report  
- 📄 Get a **simple English summary**  
- 🤖 Ask: “*Is this vitamin level normal?*” or “*What should I do next?*”  
- 📎 Export summary as **PDF** or share with your doctor  

---

## 🧰 Future Improvements

- ✅ OCR for scanned images  
- ✅ Auth with **AWS Cognito**  
- 🔜 Patient **history timeline**  
- 🔜 **Analytics dashboard** for frequent conditions  
- 🔜 Auto-**translation to regional languages**  
