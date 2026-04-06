import time
import logging
from typing import Tuple

from src.llm.model_manager import LocalLLM
from src.data.rag_manager import RAGSystem
from src.verification.why3_runner import Why3Verifier
from src.config import MAX_NEW_TOKENS, TEMPERATURE_INITIAL, TEMPERATURE_RETRY, MAX_AGENT_RETRIES

logger = logging.getLogger("AgenticProver")

class AgenticProver:
    """Orchestrates the generation, verification, and correction loop."""

    def __init__(self, llm: LocalLLM, rag: RAGSystem, verifier: Why3Verifier):
        self.llm = llm
        self.rag = rag
        self.verifier = verifier

        # Strict Prompt to prevent CPU-hogging conversational output
        self.system_prompt = (
            "Tu es un expert strict en méthodes formelles et en syntaxe Why3 (MLW).\n"
            "RÈGLE ABSOLUE: Ne génère AUCUN texte d'explication. Retourne EXCLUSIVEMENT "
            "le code source encadré par ```why3 et ```.\n"
            "Assure-toi d'utiliser 'requires', 'ensures', 'invariant', et 'variant' où nécessaire."
        )

    def run(self, instruction: str, use_rag: bool = False, use_loop: bool = False) -> Tuple[bool, int, str]:
        """Executes the pipeline for a single instruction."""
        
        # 1. Context Retrieval
        context = ""
        if use_rag:
            context = self.rag.retrieve_context(instruction)
            
        # 2. Initial Generation
        prompt = f"{self.system_prompt}\n\nINSTRUCTION:\n{instruction}"
        if context:
            prompt = f"{self.system_prompt}\n\nCONTEXTE EXPERT:\n{context}\n\nINSTRUCTION:\n{instruction}"

        logger.info("Generating initial proof...")
        start_time = time.time()
        response = self.llm.generate(prompt, temperature=TEMPERATURE_INITIAL, max_tokens=MAX_NEW_TOKENS)
        
        # 3. Verification
        is_valid, stdout, stderr, clean_code = self.verifier.verify(response)
        iterations = 1
        
        status_msg = "✅ Validé" if is_valid else "❌ Échec"
        logger.info(f"[Iteration 1] -> {status_msg} ({round(time.time() - start_time, 1)}s)")

        # 4. Agentic Self-Correction Loop
        if use_loop and not is_valid:
            for attempt in range(MAX_AGENT_RETRIES):
                logger.info(f"Initiating Correction Agent (Attempt {attempt+1}/{MAX_AGENT_RETRIES})...")
                error_msg = stderr if stderr else stdout
                
                refine_prompt = (
                    f"{self.system_prompt}\n\n"
                    f"Ton code précédent a échoué avec cette erreur de Why3/Alt-Ergo:\n{error_msg}\n\n"
                    f"Code erroné:\n```why3\n{clean_code}\n```\n\n"
                    f"Corrige les erreurs sémantiques ou de syntaxe. Renvoie uniquement le code corrigé complet."
                )
                
                retry_start = time.time()
                response = self.llm.generate(refine_prompt, temperature=TEMPERATURE_RETRY, max_tokens=MAX_NEW_TOKENS)
                is_valid, stdout, stderr, clean_code = self.verifier.verify(response)
                iterations += 1
                
                status_msg = "✅ Validé" if is_valid else "❌ Échec"
                logger.info(f"[Iteration {iterations}] -> {status_msg} ({round(time.time() - retry_start, 1)}s)")
                
                if is_valid:
                    break

        return is_valid, iterations, clean_code
