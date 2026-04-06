import os
import logging

# ==========================================
# SYSTEM CONFIGURATION
# ==========================================

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSES_DIR = os.path.join(BASE_DIR, "les_cours")
TEMP_WHY3_FILE = os.path.join(BASE_DIR, "test_temp.mlw")

# LLM Configuration
MODEL_IDENTIFIER = "google/gemma-4/transformers/gemma-4-e2b-it"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
MAX_NEW_TOKENS = 768
TEMPERATURE_INITIAL = 0.1
TEMPERATURE_RETRY = 0.2

# RAG Configuration
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
RETRIEVER_K = 2

# Verification Configuration
WHY3_BINARY = "/usr/bin/why3"
SMT_PROVER = "alt-ergo"
VERIFICATION_TIMEOUT = 30
MAX_AGENT_RETRIES = 3

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("SystemConfig")
