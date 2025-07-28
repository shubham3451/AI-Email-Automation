from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from config import settings
from llm.embedding import get_embedding_model

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANTAPI)
        self.embedding_model = get_embedding_model()
        self.collection_name = "emails_and_docs"
        self.store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model
        )

    def add_documents(self, documents, ids):
        self.store.add_documents(documents=documents, ids=ids)

    def similarity_search(self, query, k=5):
        return self.store.similarity_search(query, k=k)
