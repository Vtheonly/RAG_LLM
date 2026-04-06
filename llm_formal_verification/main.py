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

    # 5. Define Test Suite (Focused strictly on Absolute Value as the Medium benchmark)
    test_cases = [
        {
            "level": 2,
            "name": "Absolute Value",
            "prompt": "Écris une fonction `let abs (x: int) : int` qui retourne la valeur absolue de x. Ajoute ensures { result >= 0 } et ensures { result = x \/ result = -x }."
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
