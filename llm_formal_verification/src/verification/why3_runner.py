import os
import re
import shutil
import subprocess
import logging
from typing import Tuple

from src.config import WHY3_BINARY, SMT_PROVER, TEMP_WHY3_FILE, VERIFICATION_TIMEOUT

logger = logging.getLogger("Why3Runner")

class Why3Verifier:
    """Handles parsing LLM output and running it through the Why3 formal verifier."""

    def __init__(self):
        self.why3_bin = shutil.which("why3") or WHY3_BINARY
        self._ensure_installation()

    def _ensure_installation(self):
        # Auto-install if missing (useful for Colab environments)
        if not self.why3_bin or not os.path.exists(self.why3_bin):
            logger.warning("Why3 binary not found. Attempting auto-installation (Debian/Ubuntu)...")
            try:
                subprocess.run(["apt-get", "update"], capture_output=True)
                subprocess.run(["apt-get", "install", "-y", "why3", "alt-ergo"], capture_output=True)
                self.why3_bin = shutil.which("why3") or "/usr/bin/why3"
                logger.info(f"Auto-installation finished. Binary at: {self.why3_bin}")
            except Exception as e:
                logger.error(f"Auto-installation failed: {e}")
        
        # Always run config detect to ensure alt-ergo is registered
        if self.why3_bin and os.path.exists(self.why3_bin):
            logger.info("Running 'why3 config detect' to register solvers...")
            subprocess.run([self.why3_bin, "config", "detect"], capture_output=True)
        else:
            logger.error("Why3 is still missing. Verification will fail.")

    def extract_code(self, raw_response: str) -> str:
        """Extracts the MLW code block from the raw LLM response."""
        match = re.search(r'```(?:why3|mlw|ocaml)?\s*(.*?)```', raw_response, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else raw_response.strip()

    def normalize_code(self, code_str: str) -> str:
        """Ensures the code has proper module wrapping required by Why3."""
        clean_code = self.extract_code(code_str)
        
        if "module" not in clean_code.lower():
            clean_code = f"module Test\n  use int.Int\n  use ref.Ref\n\n{clean_code}\n\nend"
            
        if not clean_code.strip().lower().endswith("end"):
            clean_code = clean_code.rstrip() + "\nend"
            
        return clean_code

    def verify(self, raw_code: str) -> Tuple[bool, str, str, str]:
        """
        Writes code to file and runs Why3.
        Returns (is_valid, stdout, stderr, normalized_code).
        """
        clean_code = self.normalize_code(raw_code)
        
        with open(TEMP_WHY3_FILE, "w", encoding="utf-8") as f:
            f.write(clean_code)

        try:
            res = subprocess.run(
                [self.why3_bin, "prove", "-P", SMT_PROVER, TEMP_WHY3_FILE],
                capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT
            )
            out = res.stdout or ""
            err = res.stderr or ""
            
            # Success logic for Alt-Ergo
            is_valid = ("Valid" in out) and ("Unknown" not in out)
            return is_valid, out, err, clean_code
            
        except subprocess.TimeoutExpired:
            logger.warning("Why3 verification timed out.")
            return False, "", "Timeout", clean_code
        except Exception as e:
            logger.error(f"Verification process failed: {e}")
            return False, "", str(e), clean_code
