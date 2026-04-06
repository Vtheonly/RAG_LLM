from pathlib import Path
import re
import logging
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

from src.config import COURSES_DIR

logger = logging.getLogger("DocumentLoader")

class CourseLoader:
    """Handles the ingestion and sanitization of expert course PDFs."""

    def __init__(self, directory_path: Path = COURSES_DIR):
        self.directory_path = directory_path

    def _clean_text(self, text: str) -> str:
        """
        Pre-processes PDF slide text to remove artifacts that degrade RAG semantic matching.
        """
        # Remove excessive newlines
        text = re.sub(r'\n+', '\n', text)
        # Fix hyphenated words broken across lines
        text = re.sub(r'(?<=[a-z])-\n(?=[a-z])', '', text)
        # Strip isolated page numbers or footer metadata
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        return text

    def load_and_clean(self) -> List[Document]:
        """Loads all PDFs in the directory, cleans text, and returns Document objects."""
        docs = []
        
        # Using pathlib's glob for robust cross-platform path handling
        course_files = list(self.directory_path.glob("*.pdf"))

        if not course_files:
            logger.warning(f"No PDFs found in '{self.directory_path}'. RAG will be empty.")
            return docs

        for file_path in course_files:
            logger.info(f"Loading document: {file_path}")
            try:
                # pyMuPDFLoader accepts string paths
                loader = PyMuPDFLoader(str(file_path))

                for doc in loader.load():
                    doc.page_content = self._clean_text(doc.page_content)
                    docs.append(doc)
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")

        logger.info(f"Successfully loaded and cleaned {len(docs)} pages.")
        return docs
