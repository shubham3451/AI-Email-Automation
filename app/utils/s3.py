import json
from fastapi import UploadFile
import boto3
import os
import uuid
import mimetypes
from io import BytesIO
from PyPDF2 import PdfReader
import docx
from config import settings

s3 = boto3.client( 
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.region_name
    )
S3_BUCKET =settings.S3_BUCKET




def saveS3(body:dict):
    attachments = []
    try:
       attachment_count = body.get("attachments")
       attachment_info = json.loads(body.get("attachment-info"))
    except(ValueError, json.JSONDecodeError) as e:
        raise ValueError("Invalid metadata") from e
    
    for i in range(1, attachment_count+1):
        meta = attachment_info.get(f"attachment{i}")
        upload:UploadFile = body.get(f"attachment{i}")
        if not upload or not meta:
            continue

        filename = meta.get("filename")
        file_type = meta.get("type")
        ext = os.path.splitext(meta.get("filename", ""))[1]
        key = f"emails/{uuid.uuid4()}{ext}"
        s3.upload_fileobj(upload.file, S3_BUCKET, key)
        
        upload.file.seek(0, os.SEEK_END)
        size = upload.file.tell()
        upload.file.seek(0)

        attachment = {
            "name" : filename,
            "s3_key":key,
            "content_type":file_type,
            "filesize": size,

        }
        attachments.append(attachment)
    return attachments




def extract_text_from_s3(s3_key: str) -> str:
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=s3_key)
        content = obj['Body'].read()
    except Exception as e:
        raise RuntimeError(f"Failed to download file from S3: {e}")

    extension = os.path.splitext(s3_key)[1].lower()
    text = ""

    if extension == ".txt":
        text = content.decode("utf-8", errors="ignore")

    elif extension == ".pdf":
        try:
            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise RuntimeError(f"PDF extraction failed: {e}")

    elif extension == ".docx":
        try:
            doc = docx.Document(BytesIO(content))
            text = "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise RuntimeError(f"DOCX extraction failed: {e}")

    else:
        raise ValueError(f"Unsupported file type: {extension}")
    
    return text.strip()
