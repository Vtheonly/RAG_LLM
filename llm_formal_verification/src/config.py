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
# Search for why3 in PATH first, then common OPAM/system locations
def _find_why3():
    """Locate the why3 binary across system and OPAM paths."""
    found = shutil.which("why3")
    if found:
        return found
    # Common OPAM install paths (Colab, Linux)
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
    return "/usr/bin/why3"  # fallback

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
