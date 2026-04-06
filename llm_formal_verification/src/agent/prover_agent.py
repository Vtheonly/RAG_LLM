import time
import logging
import os
from typing import Tuple

from src.llm.model_manager import LocalLLM
from src.data.rag_manager import RAGSystem
from src.verification.why3_runner import Why3Verifier
from src.config import MAX_NEW_TOKENS, TEMPERATURE_INITIAL, TEMPERATURE_RETRY, MAX_AGENT_RETRIES, LOGS_DIR

logger = logging.getLogger("AgenticProver")

class AgenticProver:
    """Orchestrates the generation, verification, and correction loop with deep traceability."""

    def __init__(self, llm: LocalLLM, rag: RAGSystem, verifier: Why3Verifier):
        self.llm = llm
        self.rag = rag
        self.verifier = verifier

        # ENGLISH SYSTEM PROMPT + CHEAT SHEET
        # Small models reason 10x better in English. We force it to think in English, but output MLW.
        self.system_prompt = (
            "You are an expert formal verification engineer specializing in Why3 and MLW syntax.\n"
            "You will be provided with context from a university course on formal methods (in French).\n"
            "Your task is to write valid, mathematically sound Why3 code to solve the user's prompt.\n\n"
            "### WHY3 SYNTAX CHEAT SHEET ###\n"
            "module Example\n"
            "  use int.Int\n"
            "  use ref.Ref\n\n"
            "  let function_name (x: int) : int\n"
            "    requires { x >= 0 }\n"
            "    ensures  { result = x + 1 }\n"
            "  =\n"
            "    x + 1\n"
            "end\n\n"
            "### CRITICAL INSTRUCTIONS ###\n"
            "1. Output ONLY the code inside a ```why3 ... ``` block.\n"
            "2. Do NOT write any conversational text, greetings, or explanations.\n"
            "3. ALWAYS include 'module', 'requires', 'ensures', and if using loops, 'invariant' and 'variant'.\n"
            "4. Module names MUST start with a Capital letter (e.g. `module MaxFunction`, not `module max`).\n"
            "5. NEVER leave precondition brackets empty like `requires {}`. Use `requires { true }` instead."
        )

    def _write_trace_log(self, test_name: str, instruction: str, context: str, attempts: list):
        """Saves a Markdown log file so the researcher can inspect RAG and LLM decisions."""
        safe_name = test_name.replace(" ", "_").replace("/", "_").lower()
        filepath = os.path.join(LOGS_DIR, f"trace_{safe_name}_{int(time.time())}.md")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Trace Log: {test_name}\n\n")
            f.write(f"## Instruction\n{instruction}\n\n")
            f.write(f"## RAG Context Retrieved\n```text\n{context if context else 'NONE'}\n```\n\n")
            
            for i, attempt in enumerate(attempts):
                f.write(f"## Attempt {i+1}\n")
                f.write(f"**Prompt passed to LLM:**\n```text\n{attempt['prompt']}\n```\n\n")
                f.write(f"**LLM Generated Code:**\n```why3\n{attempt['code']}\n```\n\n")
                f.write(f"**Why3 Feedback (Valid: {attempt['is_valid']}):**\n```text\n{attempt['feedback']}\n```\n\n")
                
        logger.info(f"Trace saved to {filepath} for manual inspection.")

    def run(self, test_name: str, instruction: str, use_rag: bool = False, use_loop: bool = False) -> Tuple[bool, int, str]:
        """Executes the pipeline and tracks the entire history for traceability."""
        
        trace_history = []
        
        # 1. Context Retrieval
        context = ""
        if use_rag:
            context = self.rag.retrieve_context(instruction)
            
        # 2. Initial Generation
        prompt = f"{self.system_prompt}\n\nUSER INSTRUCTION:\n{instruction}"
        if context:
            prompt = f"{self.system_prompt}\n\nCOURSE CONTEXT (RAG):\n{context}\n\nUSER INSTRUCTION:\n{instruction}"

        logger.info("Generating initial proof...")
        start_time = time.time()
        response = self.llm.generate(prompt, temperature=TEMPERATURE_INITIAL, max_tokens=MAX_NEW_TOKENS)
        
        # 3. Verification
        is_valid, stdout, stderr, clean_code = self.verifier.verify(response)
        feedback_msg = stderr if stderr else stdout
        iterations = 1
        
        trace_history.append({
            "prompt": prompt, "code": clean_code, 
            "is_valid": is_valid, "feedback": feedback_msg
        })
        
        status_msg = "✅ Validé" if is_valid else "❌ Échec"
        logger.info(f"[Iteration 1] -> {status_msg} ({round(time.time() - start_time, 1)}s)")

        # 4. Agentic Self-Correction Loop
        if use_loop and not is_valid:
            for attempt in range(MAX_AGENT_RETRIES):
                logger.info(f"Initiating Correction Agent (Attempt {attempt+1}/{MAX_AGENT_RETRIES})...")
                
                refine_prompt = (
                    f"{self.system_prompt}\n\n"
                    f"Your previous Why3 code failed validation with this error:\n"
                    f"{feedback_msg}\n\n"
                    f"FAILED CODE:\n```why3\n{clean_code}\n```\n\n"
                    f"Fix the semantic or syntax errors. Return ONLY the fully corrected code block."
                )
                
                retry_start = time.time()
                response = self.llm.generate(refine_prompt, temperature=TEMPERATURE_RETRY, max_tokens=MAX_NEW_TOKENS)
                is_valid, stdout, stderr, clean_code = self.verifier.verify(response)
                feedback_msg = stderr if stderr else stdout
                iterations += 1
                
                trace_history.append({
                    "prompt": refine_prompt, "code": clean_code, 
                    "is_valid": is_valid, "feedback": feedback_msg
                })
                
                status_msg = "✅ Validé" if is_valid else "❌ Échec"
                logger.info(f"[Iteration {iterations}] -> {status_msg} ({round(time.time() - retry_start, 1)}s)")
                
                if is_valid:
                    break

        # Save the trace to a file so you can analyze the RAG/Agent behavior!
        self._write_trace_log(test_name, instruction, context, trace_history)

        return is_valid, iterations, clean_code
