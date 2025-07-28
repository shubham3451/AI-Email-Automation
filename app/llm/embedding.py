from langchain.embeddings import HuggingFaceEmbeddings
from config import settings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=settings.HUGGINGFACE_MODEL,
        cache_folder=".cache/huggingface"
    )

