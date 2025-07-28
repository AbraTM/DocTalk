# 🩺 DocTalk – Understand Your Medical Reports with AI

DocTalk is an AI-powered platform that helps non-professionals understand complex medical test reports. It generates human-readable summaries from uploaded documents (PDFs, images, text) and includes a conversational chatbot to answer health-related questions — making healthcare data truly accessible.

---

## 🚀 Features

- 🧠 LLM-powered Summarization – Translates complex lab reports into simple explanations using Gemini, OpenAI GPT, etc.
- 💬 Interactive Chatbot – Ask follow-up questions about your reports using a health-aware chatbot.
- 🖼️ PDF/Image/Text Support – Upload various file formats for interpretation.
- ☁️ AWS-Driven Asynchronous Processing – Background tasks handled via SQS, S3, and containerized workers on EC2/ECS.
- 🐳 Containerized Services – Easy deployment with Docker and Docker Compose.
- 🧾 Poppler-Powered PDF Parsing – OCR and PDF support with Poppler utilities on the worker.
- 🌐 Modern Tech Stack – Built with FastAPI, ReactJS, and designed for scalability.

---

## 🧱 Tech Stack

| Layer            | Technology                    |
|------------------|-------------------------------|
| Frontend         | NextJS                        |
| Backend API      | FastAPI                       |
| LLM Integration  | Gemini Pro                    |
| Storage          | AWS S3                        |
| Async Tasks      | AWS SQS + EC2 (Worker Service)|
| Auth             | Firebase                      |
| Containerization | Docker + Docker Compose       |

---

## 🧪 Sample Use Cases

- 📤 Upload your **CBC, LFT, or X-ray** report  
- 📄 Get a **simple English summary**  
- 🤖 Ask: “*Is this vitamin level normal?*” or “*What should I do next?*”  

---

## 🧰 Future Improvements

- ✅ OCR for scanned images  
- ✅ Auth with **AWS Cognito**  
- 🔜 Patient **history timeline**  
- 🔜 **Analytics dashboard** for frequent conditions  
- 🔜 Auto-**translation to regional languages**  
