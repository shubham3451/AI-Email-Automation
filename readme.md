# 🤖 AI Auto Email Reply System

An intelligent, context-aware email reply system that automatically responds to customer emails using Large Language Models (LLMs), vector search over internal documents, and prior thread context.

Built with FastAPI, PostgreSQL, AWS S3, LangChain, Hugging Face LLMs, Celery, Redis, and Qdrant — all fully containerized with Docker.

---

## 🚀 Features

- 🔗 **Webhook endpoint** for receiving incoming customer emails
- 💾 **PostgreSQL** stores emails, replies, and thread history
- 📎 **Attachments uploaded to AWS S3** and metadata saved in DB
- 📬 **Replies generated using LLMs** via Hugging Face (e.g., Falcon, Mistral)
- 📚 **Context-aware vector similarity search** via Qdrant (for policy/docs retrieval)
- ⚙️ **Background processing with Celery & Redis** to keep API snappy
- 🧠 **LangChain** orchestrates prompt templates and LLM chains
- 🐳 Fully containerized with Docker and `docker-compose`

---

## 🧱 System Architecture

```text
            ┌───────────────┐
            │ Incoming Email│
            └──────┬────────┘
                   ▼
       ┌────────────────────────┐
       │ FastAPI Webhook (/api) │
       └────────┬───────────────┘
                ▼
        Save to PostgreSQL
                ▼
         Upload to AWS S3
                ▼
     Trigger Celery background task
                ▼
     ┌─────────────────────────────┐
     │ Celery Task: Process Email  │
     └────────────┬────────────────┘
                  ▼
        Embed + Query Qdrant Vector DB
                  ▼
     Generate human-like reply via LLM
                  ▼
        Save response to PostgreSQL
````

---

## 📦 Tech Stack

| Layer           | Technology                     |
| --------------- | ------------------------------ |
| API             | FastAPI                        |
| Background Jobs | Celery + Redis                 |
| Database        | PostgreSQL                     |
| Object Storage  | AWS S3                         |
| LLMs            | Hugging Face Hub via LangChain |
| Embedding Store | Qdrant (Vector DB)             |
| Orchestration   | Docker + Docker Compose        |

---

## 📁 Project Structure

```
email_auto_reply/
├── app/
│   ├── api/                # Webhook route
│   ├── celery_worker.py    # Celery worker entry
│   ├── config.py           # Environment and settings
│   ├── db/                 # PostgreSQL models and session
│   ├── llm/                # LangChain + Qdrant + reply generator
│   ├── tasks/              # Background email processing task
│   ├── utils/              # S3, file parsing, filtering, etc.
│   └── main.py             # FastAPI app entrypoint
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Environment Variables

`.env` file:

```env
# PostgreSQL
DATABASE_URL=postgresql://emailuser:strongpassword@db:5432/emaildb

# Celery
CELERY_BROKER_URL=redis://redis:6379/0

# AWS S3
aws_access_key_id=your-key
aws_secret_access_key=your-secret
region_name=us-east-1
S3_BUCKET=email-attachments

# Qdrant
QDRANT_URL=http://qdrant:6333

# Hugging Face
HUGGINGFACETOKEN=hf_your_token
HUGGINGFACE_MODEL=tiiuae/falcon-7b-instruct

# Support settings
SUPPORT_EMAIL=support@example.com
WEBHOOK_SECRET=your-webhook-verification-token
```

---

## 🐳 Running with Docker

### 1. Build and run the app

```bash
docker-compose up --build
```

### 2. Access the services

* **API**: [http://localhost:8000](http://localhost:8000)
* **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **PostgreSQL**: exposed on port 5432
* **Qdrant UI (optional)**: if included, [http://localhost:6333](http://localhost:6333)

---

## 🔧 Development

### Start FastAPI locally

```bash
uvicorn app.main:app --reload
```

### Start Celery worker

```bash
celery -A app.celery_worker.celery worker --loglevel=info
```

## 🧠 How Replies Are Generated

1. The incoming email and attachments are parsed and uploaded.
2. A background Celery task is triggered.
3. Email content is embedded and compared via Qdrant against internal documents or policies.
4. LangChain constructs a prompt combining:

   * Thread history
   * Attachment contents (PDFs, DOCX, etc.)
   * Similar documents from Qdrant
   * Latest customer message
5. Hugging Face LLM generates a reply.
6. The reply is saved back to the database and optionally emailed.

---

## 🛡️ Security Best Practices

* ✅ Validate webhook requests using `WEBHOOK_SECRET`
* 🔐 Store AWS and HF tokens securely (e.g., secrets manager)
* ⛔ Never log sensitive email contents or API tokens



