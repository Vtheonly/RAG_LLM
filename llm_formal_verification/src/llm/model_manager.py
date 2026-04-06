import torch
import kagglehub
import logging
from transformers import AutoProcessor, AutoModelForCausalLM
from src.config import MODEL_IDENTIFIER

logger = logging.getLogger("ModelManager")

class LocalLLM:
    """Handles the loading and inference of the local HuggingFace/Kagglehub model."""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = None
        self.model = None

    def load_model(self):
        """Downloads and loads the Gemma 4 model into memory with CPU optimizations."""
        logger.info(f"Downloading/Locating model: {MODEL_IDENTIFIER}")
        model_path = kagglehub.model_download(MODEL_IDENTIFIER)

        logger.info(f"Loading model onto {self.device.upper()} (bfloat16 precision)...")
        self.processor = AutoProcessor.from_pretrained(model_path)
        
        # Using bfloat16 is crucial for keeping CPU memory footprint low
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map="auto"
        )
        logger.info("Model successfully loaded into memory.")

    def generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generates text using the loaded model."""
        if not self.model or not self.processor:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        messages = [{"role": "user", "content": prompt}]
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        inputs = self.processor(text=text, return_tensors="pt").to(self.model.device)
        input_len = inputs["input_ids"].shape[-1]

        # Use inference_mode for faster CPU execution
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True if temperature > 0 else False
            )
            
        response = self.processor.decode(outputs[0][input_len:], skip_special_tokens=True)
        return response.strip()
