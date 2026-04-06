import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import List, Dict

from src.agent.prover_agent import AgenticProver
from src.config import MODEL_IDENTIFIER

logger = logging.getLogger("Evaluator")

class Evaluator:
    """Runs benchmarks and visualizes results."""

    def __init__(self, agent: AgenticProver):
        self.agent = agent

    def run_suite(self, test_cases: List[Dict]) -> pd.DataFrame:
        results = []

        logger.info("=== STARTING EVALUATION SUITE ===")
        for tc in test_cases:
            logger.info(f"\n>> TEST NIVEAU {tc['level']} : {tc['name']}")

            logger.info("--- [1] BASELINE (Zero-shot) ---")
            v, it, _ = self.agent.run(tc['name'], tc['prompt'], use_rag=False, use_loop=False)
            results.append({"Niveau": tc['level'], "Test": tc['name'], "Méthode": "1. Baseline", "Succès": v, "Itérations": it})

            logger.info("--- [2] RAG (Contextual) ---")
            v, it, _ = self.agent.run(tc['name'], tc['prompt'], use_rag=True, use_loop=False)
            results.append({"Niveau": tc['level'], "Test": tc['name'], "Méthode": "2. RAG", "Succès": v, "Itérations": it})

            logger.info("--- [3] FULL AGENTIC LOOP ---")
            v, it, final_code = self.agent.run(tc['name'], tc['prompt'], use_rag=True, use_loop=True)
            results.append({"Niveau": tc['level'], "Test": tc['name'], "Méthode": "3. Full Agent", "Succès": v, "Itérations": it})
            
            if v:
                logger.info(f"Valid Code Generated:\n{final_code}")

        return pd.DataFrame(results)

    def plot_results(self, df: pd.DataFrame, save_path: str = "evaluation_chart.png"):
        """Generates the comparison chart based on the Master 2 specification."""
        df["Succès (%)"] = df["Succès"].astype(int) * 100

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x="Niveau", y="Succès (%)", hue="Méthode", palette="viridis")
        plt.title(f"Taux de Validation Formelle Why3\nModèle: {MODEL_IDENTIFIER.split('/')[-1]}")
        plt.xlabel("Complexité (1=Simple, 2=Boucle, 3=Hardcore)")
        plt.ylabel("Validé par Alt-Ergo (%)")
        plt.ylim(0, 110)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title="Méthode")
        plt.tight_layout()
        
        plt.savefig(save_path)
        logger.info(f"Plot saved to {save_path}")
        # plt.show() # Uncomment if running in Jupyter, kept commented for pure CLI script
