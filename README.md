# 🩺 DocTalk – Understand Your Medical Reports with AI

DocTalk is an AI-powered platform that helps non-professionals make sense of complex medical reports.
Upload your health documents (PDFs, images, or text) and get clear, human-readable summaries, plus a conversational chatbot that can answer health-related questions in real time.

Goal: Make healthcare data truly accessible to everyone.

---

## Features

- LLM-Powered Summarization – Converts complex lab results into plain-language explanations using Gemini Pro, OpenAI GPT, and other models.

- Interactive Chatbot – Ask follow-up questions about your reports with a health-aware AI assistant.

- Multi-Format Support – Works with PDFs, scanned images, and plain text reports.

- AWS-Driven Asynchronous Processing – Background tasks handled via SQS, S3, and containerized workers running on EC2.

- Containerized Services – Consistent deployments using Docker and Docker Compose.

- Poppler-Powered PDF Parsing – Supports OCR and advanced PDF handling.

- Modern & Scalable Stack – Built with Next.js (frontend) and FastAPI (backend) for performance and flexibility.

- Firebase Authentication – Secure and simple sign-in for users..

---

## Tech Stack

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

## Sample Use Cases

-  Upload your **Blood Test, ECG Scans, or X-ray** report  
-  Get a **simple English summary**  
-  Ask: “*Is this vitamin level normal?*” or “*What should I do next?*”  

---

## Future Improvements

- Chat history view & retrieval – let users access and browse their past conversations
- Multi-report health analysis – combine multiple reports for overall health summaries and trends
- Patient history timeline – visualize health changes over time
