from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import session
from ..db.models import Email, Attachment
from ..db.session import get_db
from ..utils.verify_signature import verify_signature
from ..utils.s3 import saveS3
from email import message_from_string
from datetime import datetime
from ..tasks.email_processor import process_email


router = APIRouter()

router.post("/api/webhook")
async def get_email(request:Request,
    x_twilio_email_event_webhook_signature: str = Header(...),
    x_twilio_email_event_webhook_timestamp: str = Header(...),
    db : session=Depends(get_db)
    ):

    raw_body = await request.body()
    is_valid = verify_signature(x_twilio_email_event_webhook_timestamp, raw_body, x_twilio_email_event_webhook_signature)
    if not is_valid:
        raise HTTPException(status_code=401, detail="invalid signature")
    

    body = await request.form()    
    
    sender_address = body.get("from")
    reciever_address = body.get("to")
    subject   = body.get("subject")
    text_body = body.get("text")
    
    if not sender_address or not reciever_address:
        raise HTTPException(400, "Missing `from` or `to`")
    

    headers_raw = body.get("headers", "")
    parsed_headers = message_from_string(headers_raw)

    message_id = parsed_headers.get("Message-ID")
    reply_to = parsed_headers.get("In-Reply-To")
    replied_email = None
    if reply_to:
        replied_email = db.query(Email).filter(Email.message_id==reply_to).first()
        

    email = Email(
        sender_address = sender_address,
        reciever_address=reciever_address,
        subject=subject,
        body=text_body,
        timestamp=datetime.utcnow(),
        reply_to_id = replied_email.id if replied_email else None ,
        message_id=message_id
    )
    db.add(email)
    db.commit()
    db.refresh(email)
    attachment_data = saveS3(body)
    for att in attachment_data:
       db_attachment = Attachment(
           name=att["name"],
           s3_key=att["s3_key"],
           content_type=att["content_type"],
           file_size=att["file_size"],
           email_id=email.id 
       )
       db.add(db_attachment)
    db.commit()

    process_email.delay(email.id)
    return {"status": "success"}
