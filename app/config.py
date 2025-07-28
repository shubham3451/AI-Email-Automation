import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    aws_access_key_id: str = os.getenv("aws_access_key_id")
    aws_secret_access_key: str = os.getenv("aws_secret_access_key")
    region_name: str = os.getenv("region_name")
    S3_BUCKET: str = os.getenv("S3_BUCKET")
    QDRANTAPI: str = os.getenv("QDRANT_URL")
    HUGGINGFACETOKEN: str = os.getenv("HUGGINGFACETOKEN")
    HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    SUPPORT_EMAIL: str = os.getenv("SUPPORT_EMAIL")
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET")

    class Config:
        env_file = ".env"

settings = Settings()



