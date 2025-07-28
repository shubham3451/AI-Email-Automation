from fastapi import FastAPI
from app.api import webhook

app = FastAPI(
    title="Email Auto Reply Service",
    description="Automatically generates replies to customer emails using LLMs.",
    version="1.0.0"
)


app.include_router(webhook.router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Email Auto Reply Service is running."}

