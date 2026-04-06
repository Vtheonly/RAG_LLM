import os
import shutil
import logging

# ==========================================
# SYSTEM CONFIGURATION
# ==========================================

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSES_DIR = os.path.join(BASE_DIR, "les_cours")
TEMP_WHY3_FILE = os.path.join(BASE_DIR, "test_temp.mlw")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# LLM Configuration
MODEL_IDENTIFIER = "google/gemma-4/transformers/gemma-4-e2b-it"
# Switched to E5: Much better for French + Code context retrieval
EMBEDDING_MODEL = "intfloat/multilingual-e5-small" 
MAX_NEW_TOKENS = 1024
TEMPERATURE_INITIAL = 0.1
TEMPERATURE_RETRY = 0.3

# RAG Configuration - CRITICAL FIX
# 400 is too small for code. 1500 ensures whole functions are retrieved intact.
CHUNK_SIZE = 1500 
CHUNK_OVERLAP = 200
RETRIEVER_K = 3

# Verification Configuration
def _find_why3():
    """Locate the why3 binary across system and OPAM paths."""
    found = shutil.which("why3")
    if found:
        return found
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".opam", "default", "bin", "why3"),
        os.path.join(home, ".opam", "4.14.2", "bin", "why3"),
        "/usr/local/bin/why3",
        "/usr/bin/why3",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return "/usr/bin/why3"

WHY3_BINARY = _find_why3()
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
