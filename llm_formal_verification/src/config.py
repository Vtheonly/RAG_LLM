import os
import shutil
import logging
from pathlib import Path

# ==========================================
# SYSTEM CONFIGURATION
# ==========================================

# Base directory (absolute path to the root of the project)
BASE_DIR = Path(__file__).resolve().parent.parent
COURSES_DIR = BASE_DIR / "les_cours"
COURSES_MD_DIR = BASE_DIR / "les_md_cours"
TEMP_WHY3_FILE = BASE_DIR / "test_temp.mlw"
LOGS_DIR = BASE_DIR / "logs"

# RAG Mode: "pdf" or "md"
RAG_MODE = "md"

# Ensure crucial directories exist
COURSES_DIR.mkdir(exist_ok=True)
COURSES_MD_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# LLM Configuration
MODEL_IDENTIFIER = "google/gemma-4/transformers/gemma-4-e2b-it"
EMBEDDING_MODEL = "intfloat/multilingual-e5-small" 
MAX_NEW_TOKENS = 1024
TEMPERATURE_INITIAL = 0.1
TEMPERATURE_RETRY = 0.3

# RAG Configuration
CHUNK_SIZE = 1500 
CHUNK_OVERLAP = 200
RETRIEVER_K = 3

# Verification Configuration
def _find_why3():
    """Locate the why3 binary across system, OPAM, and Windows paths."""
    # 1. Search in system PATH
    found = shutil.which("why3")
    if found:
        return found
    
    # 2. Search in common OPAM/Linux paths
    home = Path.home()
    candidates = [
        home / ".opam" / "default" / "bin" / "why3",
        home / ".opam" / "4.14.2" / "bin" / "why3",
        Path("/usr/local/bin/why3"),
        Path("/usr/bin/why3"),
    ]
    
    for c in candidates:
        if c.is_file():
            return str(c)
            
    # 3. Fallback for Windows users (placeholder if they have it in local bin)
    return "why3"  # Default attempt

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

