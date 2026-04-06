import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import List, Dict

from src.agent.prover_agent import AgenticProver
from src.config import MODEL_IDENTIFIER, BASE_DIR

logger = logging.getLogger("Evaluator")

class Evaluator:
    """Runs benchmarks and visualizes results."""

    def __init__(self, agent: AgenticProver):
        self.agent = agent

    def run_suite(self, test_cases: List[Dict]) -> pd.DataFrame:
        results = []
        report_lines = ["# 🔬 Final Research Capability Report\n", f"Model: {MODEL_IDENTIFIER}\n", "--- \n"]

        logger.info("=== STARTING EVALUATION SUITE ===")
        for tc in test_cases:
            logger.info(f"\n>> TEST NIVEAU {tc['level']} : {tc['name']}")

            logger.info("--- [1] BASELINE (Zero-shot) ---")
            v1, it1, _ = self.agent.run(tc['name'], tc['prompt'], use_rag=False, use_loop=False)
            results.append({"Niveau": tc['level'], "Test": tc['name'], "Méthode": "1. Baseline", "Succès": v1, "Itérations": it1})

            logger.info("--- [2] RAG (Contextual) ---")
            v2, it2, _ = self.agent.run(tc['name'], tc['prompt'], use_rag=True, use_loop=False)
            results.append({"Niveau": tc['level'], "Test": tc['name'], "Méthode": "2. RAG", "Succès": v2, "Itérations": it2})

            logger.info("--- [3] FULL AGENTIC LOOP ---")
            v3, it3, final_code = self.agent.run(tc['name'], tc['prompt'], use_rag=True, use_loop=True)
            results.append({"Niveau": tc['level'], "Test": tc['name'], "Méthode": "3. Full Agent", "Succès": v3, "Itérations": it3})
            
            res_str = "SUCCESS ✅" if v3 else "FAILURE ❌"
            report_lines.append(f"### Test: {tc['name']} (Level {tc['level']})\n")
            report_lines.append(f"- **Result**: {res_str}\n")
            report_lines.append(f"- **Iterations**: {it3}\n")
            if v3:
                report_lines.append(f"- **Final Proved Code**:\n```why3\n{final_code}\n```\n")
            else:
                report_lines.append("- **Status**: Model could not satisfy the SMT solver within retry limits.\n")
            report_lines.append("\n---\n")

        # Save Final Report
        from src.config import LOGS_DIR
        import time
        report_path = LOGS_DIR / f"final_report_{int(time.time())}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.writelines(report_lines)
        logger.info(f"Final research report saved to {report_path}")

        return pd.DataFrame(results)

    def plot_results(self, df: pd.DataFrame, save_path: str = "evaluation_chart.png"):
        """Generates the comparison chart based on the Master 2 specification."""
        df["Succès (%)"] = df["Succès"].astype(int) * 100
        
        # Ensure save path is in the base directory
        final_path = BASE_DIR / save_path

        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x="Niveau", y="Succès (%)", hue="Méthode", palette="viridis")
        plt.title(f"Taux de Validation Formelle Why3\nModèle: {MODEL_IDENTIFIER.split('/')[-1]}")
        plt.xlabel("Complexité (1=Simple, 2=Boucle, 3=Hardcore)")
        plt.ylabel("Validé par Alt-Ergo (%)")
        plt.ylim(0, 110)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title="Méthode")
        plt.tight_layout()
        
        plt.savefig(str(final_path))
        logger.info(f"Plot saved to {final_path}")
        # plt.show() # Uncomment if running in Jupyter, kept commented for pure CLI script
