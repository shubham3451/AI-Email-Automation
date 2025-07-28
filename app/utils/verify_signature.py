import hmac
import base64
import hashlib
from config import settings


def verify_signature(timestamp:str, body:bytes, signature:str):
    message = timestamp.encode() + body
    computed_hmac = hmac.new(settings.WEBHOOK_SECRET.encode(), message,hashlib.sha256).digest()
    encoded_hmac = base64.b64encode(computed_hmac).decode()

    return hmac.compare_digest(encoded_hmac, signature)
