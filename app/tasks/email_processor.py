from celery import Celery
from db.session import SessionLocal
from db.models import Email
from llm.vector_store import VectorStore
from llm.prompt import generate_reply
from utils.filters import needs_document_lookup
from utils.s3 import extract_text_from_s3
from langchain.docstore.document import Document
from config import settings
import os

celery = Celery("worker", broker=settings.CELERY_BROKER_URL)
vector_store = VectorStore()

@celery.task
def process_email(email_id: int):
    db = SessionLocal()
    email = db.query(Email).get(email_id)

    # Build full thread history (from root to current)
    thread_emails = []
    ptr = email
    while ptr:
        thread_emails.append(ptr)
        ptr = ptr.reply_to
    thread_emails.reverse()

    thread_formatted = "\n\n".join(
        f"{'You' if e.is_outgoing else e.sender_address}: {e.body or ''}"
        for e in thread_emails
    )

    # Extract text from attachments
    attachment_texts = [extract_text_from_s3(att.s3_key) for att in email.attachments]
    attachments_combined = "\n\n".join(attachment_texts)

    # Embed email + attachments into vector DB
    doc = Document(
        page_content=(email.body or "") + "\n\n" + attachments_combined,
        metadata={"source": "email", "email_id": str(email.id)}
    )
    vector_store.add_documents([doc], ids=[str(email.id)])

    # Decide if need to retrieve documents
    if needs_document_lookup(email.body):
        docs = vector_store.similarity_search(email.body, k=5)
        docs_combined = "\n\n".join(d.page_content for d in docs if d.metadata.get("source") != "email")
    else:
        docs_combined = ""

    # Generate reply using LLM
    reply_text = generate_reply(thread_formatted, attachments_combined, docs_combined, email.body or "")

    # Save reply email to DB
    reply_email = Email(
        sender_address=settings.SUPPORT_EMAIL,
        receiver_address=email.sender_address,
        subject=f"Re: {email.subject or ''}",
        body=reply_text,
        is_outgoing=True,
        reply_to_id=email.id
    )
    db.add(reply_email)
    db.commit()
    db.close()

    # send reply email through SMTP or 3rd party API

