import sys
import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from src.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, RETRIEVER_K

logger = logging.getLogger("RAGManager")

# SQLite fix for ChromaDB compatibility in certain local environments
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

class RAGSystem:
    """Manages text chunking, embedding, and vector retrieval."""

    def __init__(self):
        self.vectorstore = None
        self.retriever = None

    def initialize_database(self, documents: List[Document]):
        """Splits documents and initializes the ChromaDB vector store."""
        if not documents:
            logger.warning("No documents provided to RAG system.")
            return

        logger.info("Splitting documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        splits = splitter.split_documents(documents)

        logger.info(f"Initializing HuggingFace Embeddings ({EMBEDDING_MODEL})...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        logger.info("Building Chroma Vector Store...")
        self.vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
        logger.info("RAG Database Ready.")

    def retrieve_context(self, query: str) -> str:
        """Retrieves top-K relevant chunks for a given query."""
        if not self.retriever:
            return ""
        
        try:
            retrieved_docs = self.retriever.invoke(query)
            context = "\n...\n".join([d.page_content for d in retrieved_docs])
            return context
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return ""
