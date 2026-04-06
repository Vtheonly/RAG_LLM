import logging
from src.data.document_loader import CourseLoader
from src.data.rag_manager import RAGSystem
from src.llm.model_manager import LocalLLM
from src.verification.why3_runner import Why3Verifier
from src.agent.prover_agent import AgenticProver
from src.evaluation.evaluator import Evaluator

def main():
    logger = logging.getLogger("Main")
    logger.info("Booting Learning-Infused Formal Reasoning System...")

    # 1. Initialize Components
    loader = CourseLoader()
    rag = RAGSystem()
    llm = LocalLLM()
    verifier = Why3Verifier()

    # 2. Data Ingestion & RAG Setup
    documents = loader.load_and_clean()
    rag.initialize_database(documents)

    # 3. LLM Setup (Downloads and maps to CPU/GPU)
    llm.load_model()

    # 4. Agent Setup
    agent = AgenticProver(llm=llm, rag=rag, verifier=verifier)
    evaluator = Evaluator(agent=agent)

    # 5. Define Test Suite (Expanded for deep analysis)
    test_cases = [
        {
            "level": 1,
            "name": "Dummy Max",
            "prompt": "Écris une fonction `let max (x y: int) : int` qui retourne le plus grand entier. Ajoute `requires { true }` et un `ensures` correct."
        },
        {
            "level": 1,
            "name": "Absolute Value",
            "prompt": "Écris une fonction `let abs (x: int) : int` qui retourne la valeur absolue de x. Ajoute ensures { result >= 0 } et ensures { result = x \\/ result = -x }."
        },
        {
            "level": 2,
            "name": "Somme Iterative",
            "prompt": "Écris une fonction `let sum_to_n (n: int) : int` utilisant une boucle while. Ajoute `requires { n >= 0 }` et `ensures { result >= 0 }`. Inclus un invariant et un variant de terminaison."
        },
        {
            "level": 3,
            "name": "Div Euclidienne",
            "prompt": "Écris `let div_euclidienne (a b: int) : (int, int)` par soustractions successives. requires a >= 0 et b > 0. L'invariant doit contenir a = b * q + r. N'oublie pas le variant."
        }
    ]

    # 6. Run Evaluation
    df_results = evaluator.run_suite(test_cases)
    
    print("\n===============================")
    print("      FINAL RESULTS TABLE")
    print("===============================\n")
    print(df_results.to_string(index=False))

    # 7. Visualize
    evaluator.plot_results(df_results)
    print("\n✅ Run complete. Check the 'logs/' directory to inspect RAG contexts and LLM reasoning.")

if __name__ == "__main__":
    main()
