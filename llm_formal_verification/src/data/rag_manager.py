import sys
import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from src.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, RETRIEVER_K

logger = logging.getLogger("RAGManager")

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

        logger.info(f"Splitting documents into chunks of {CHUNK_SIZE} characters...")
        # Using a more code-friendly split approach
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\nmodule", "\nlet", "\n\n", "\n", " ", ""]
        )
        splits = splitter.split_documents(documents)

        logger.info(f"Initializing HuggingFace Embeddings ({EMBEDDING_MODEL})...")
        # Ensure we add the query instruction prefix required by e5 models
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        logger.info("Building Chroma Vector Store...")
        self.vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
        logger.info("RAG Database Ready.")

    def _sanitize_context(self, text: str) -> str:
        """Translates Unicode math symbols in notes to Why3-legal ASCII."""
        replacements = {
            "∧": "&&",
            "∨": "||",
            "¬": "not",
            "⇒": "->",
            "⇔": "<->",
            "∀": "forall",
            "∃": "exists",
            "≠": "<>"
        }
        for char, target in replacements.items():
            text = text.replace(char, target)
        return text

    def retrieve_context(self, query: str) -> str:
        """Retrieves top-K relevant chunks for a given query and sanitizes them."""
        if not self.retriever:
            return ""
        
        try:
            # E5 models require 'query: ' prefix for optimal retrieval
            e5_query = f"query: {query}"
            retrieved_docs = self.retriever.invoke(e5_query)
            
            context_blocks = []
            for i, d in enumerate(retrieved_docs):
                source = d.metadata.get('source', 'Unknown Source')
                page = d.metadata.get('page', 'Unknown Page')
                
                # SANITIZE: Mathematical symbols in notes confuse the 2B model
                clean_content = self._sanitize_context(d.page_content)
                context_blocks.append(f"--- SOURCE: {source} (Page {page}) ---\n{clean_content}")
                
            return "\n\n".join(context_blocks)
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return ""
