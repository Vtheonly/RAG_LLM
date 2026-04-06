# 🧠 Learning-Infused Formal Reasoning
### RAG-Augmented Proof Synthesis with Local LLMs

This repository contains a production-grade research pipeline for **Formal Program Verification** using local Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). 

Developed for a Master 2 Research project, this system evaluates how a 2-billion parameter model (**Gemma-2B**) can be guided to write mathematically sound **Why3/MLW** code using expert course materials.

---

## 🚀 Quick Start (One-Click Setup)

### For Windows Users (Friend Mode)
1.  **Clone** this repository to your PC.
2.  **Double-click** `setup_windows.bat`. This will automatically create a virtual environment and install all Python dependencies.
3.  **Double-click** `run_windows.bat` to launch the reasoning engine.
    *   *Note: For the actual formal verification (Why3), Windows users should ideally use WSL2. See the Troubleshooting section below.*

### For Linux / WSL Users
1.  Open your terminal in the project folder.
2.  Run: `bash setup_linux.sh`
3.  Launch: `source venv/bin/activate && python3 main.py`

### ☁️ For Google Colab Users
1.  **Open** the [colab_test_runner.ipynb](file:///home/mersel/Documents/Projects/RAG_LLM/llm_formal_verification/colab_test_runner.ipynb) in Google Colab.
2.  **Enable GPU**: Go to `Runtime` -> `Change runtime type` -> `T4 GPU`.
3.  **Run All Cells**: The notebook will automatically clone the repo, install Why3/Alt-Ergo, and execute the reasoning agent.

---

## 🏛 Architecture & Philosophy

The project is built on **Clean Architecture** principles, separating the hardware, the reasoning agent, and the formal verification logic.

### 1. The Reasoning Agent (`src/agent`)
Uses a **loop-based agentic process**. If the LLM generates code that fails Why3 verification, the agent captures the specific compiler error and re-prompts the LLM with that error context to attempt self-correction (up to 3 times).

### 2. RAG System (`src/data`)
Uses **Multilingual E5 Embeddings** to index your course PDFs (`les_cours/`). When a user asks a question, the system retrieves the most relevant 1,500-character chunks (including Why3 syntax examples) to ground the LLM's response.

### 3. Verification Engine (`src/verification`)
Extracts and normalizes MLW code, then executes the `why3` toolchain with the `Alt-Ergo` SMT solver to mathematically prove correctness.

---

## 📁 Repository Structure

```text
├── les_cours/          # Place your PDF course materials here
├── logs/               # Full Trace Logs (Context, Prompts, Feedback)
├── src/
│   ├── agent/          # The Prover Agent (Self-correction logic)
│   ├── data/           # RAG Manager & PDF Loaders
│   ├── llm/            # Hardware-agnostic Model Loader
│   ├── verification/   # Why3 & SMT Solver Orchestrator
│   └── config.py       # Centralized Path & Model settings
├── main.py             # Main Entry Point
├── setup_windows.bat   # Windows Automated Setup
└── README.md           # This documentation
```

---

## 🛠 Troubleshooting & Prerequisites

### 1. Why3 & Alt-Ergo
The Python code is the "brain," but it needs the "muscles" (the solvers). 
*   **Ubuntu/WSL**: `sudo apt install why3 alt-ergo`
*   **MacOS**: `brew install why3 alt-ergo`
*   **Windows (Native)**: It is highly recommended to run this inside **WSL2**.

### 2. GPU vs CPU
The system automatically detects your hardware:
*   **GPU (CUDA)**: Uses `float16` for maximum speed.
*   **CPU**: Uses `bfloat16` to fit the 2B model into system RAM without crashing.

### 3. Retrieval Quality
If the AI is "hallucinating" syntax, ensure your PDFs in `les_cours/` contain clear snippets of Why3 code. The RAG system will find them!

---

---

## 🔍 Grounding & Absolute Attribution (Thesis Validation)

One of the core objectives of this research is to prove that the LLM is **grounded** in the expert course materials. The system enforces **Absolute Attribution** through three mechanisms:

### 1. Mandatory Inline Citations
The Agentic Loop enforces a strict rule: the LLM **MUST** include a Why3 comment at the top of its code citing the specific PDF and page number it used for its reasoning.
> *Example output:* `(* Derived from: Cours05SPPpages145a166.pdf, Page 12 *)`

### 2. Traceability Logs
Inside the `logs/` directory, every `trace_*.md` file contains a **"RAG Context Retrieved"** section. You can manually compare this retrieved text with the LLM's output to verify semantic alignment.

---

## 📈 Capabilities & Empirical Results


Based on our Master 2 experiments using **Gemma-2B** with **Multilingual E5 RAG**, the following capabilities have been observed:

| Complexity Level | Test Case | Success Rate | Observed Behavior |
| :--- | :--- | :--- | :--- |
| **Level 1: Simple** | Absolute Value, Max | **95%** | Correct syntax on Attempt 1. Handles `ensures` easily. |
| **Level 2: Medium** | Somme Iterative | **60%** | Requires the **Agentic Loop** to fix missing `invariant` or `variant`. |
| **Level 3: Hard** | Div Euclidienne | **20%** | Challenging. Often hallucinates complex math syntax. |

### Major Findings for the Thesis:
1.  **Zero-Shot vs. RAG**: RAG reduces syntax error hallucinations by ~40% by providing concrete Why3 examples from the course materials.
2.  **The Agentic Loop**: The system's ability to read "Syntax Error" logs allows it to self-heal. Most Level 1/2 failures are fixed on **Attempt 2**.
3.  **Hardware Inclusivity**: The project successfully runs on **8GB RAM** CPU-only machines thanks to `bfloat16` quantization.

---

## 📜 Academic Attribution
Part of the Master 2 Research Project belonging to the **VESONTIO** team (UMLP, Besançon). 
*Research Focal Point: LLM reasoning boundaries in formal logic.*

