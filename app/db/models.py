from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from datetime import datetime

Base = declarative_base()

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    sender_address = Column(String(255), index=True, nullable=False)
    receiver_address = Column(String(255), index=True, nullable=False)
    subject = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_outgoing = Column(Boolean, default=False, nullable=False)
    reply_to_id = Column(Integer, ForeignKey("emails.id"), nullable=True)
    message_id = Column(String(255), unique=True, nullable=True)
    attachments = relationship("Attachment", back_populates="email", cascade="all, delete-orphan")
    reply_to = relationship("Email", remote_side=[id])

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    s3_key = Column(String(512), nullable=False)
    content_type = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    email = relationship("Email", back_populates="attachments")


