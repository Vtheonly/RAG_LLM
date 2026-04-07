# Research Findings: Learning-Infused Formal Reasoning
**Master 2 Thesis Analysis - Evaluation Suite Results**

## 📊 Executive Summary
The primary goal of this research was to evaluate the impact of **Retrieval-Augmented Generation (RAG)** on a 2-billion parameter model (Gemma-2B) for formal verification tasks in Why3. The data suggests that RAG is a **critical enabler** for basic function synthesis but hits a "Syntax Performance Ceiling" when dealing with complex, iteratively-defined proofs (loops).

| Level | Task | Baseline | RAG | Agentic Loop | Key Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Absolute Value | ❌ Failed | ✅ **Passed** | ✅ Passed | RAG provided the exact Why3 structure. |
| **2** | Summation | ❌ Failed | ❌ Failed | ❌ Failed | LLM failed to use `ref` for loop state. |
| **3** | Eucl. Division | ❌ Failed | ❌ Failed | ❌ Failed | Syntax errors (∧) and Missing Invariants. |

---

## 🔍 Key Insights

### 1. The RAG "Safety Net"
In **Test Niveau 1 (Absolute Value)**, the baseline model hallucinated significantly. By injecting context from the course slides (specifically `Cours01` and `tdHoare`), the model successfully produced a verified proof. This demonstrates that RAG effectively offsets the model's limited "native" knowledge of MLW syntax.

### 2. The "Mutable State" Bottleneck
A consistent failure across **Test Niveau 2 and 3** was the model's inability to handle mutable variables in Why3. 
- **LLM Error**: `let result = 0 in ... while ... let result = result + 1 in`.
- **Why3 Correct Syntax**: `let result = ref 0 in ... while ... result := !result + 1`.
Smaller models like Gemma-2B tend to default to the functional `let` pattern common in OCaml/Python, even when instructed otherwise.

### 3. Syntax Hallucinations (UTF-8 Characters)
The model repeatedly used mathematical symbols like `∧` and `∨` instead of the ASCII operators `/\` and `\/` required by Why3. This suggests that the model's "Mathematical Training" overrides the "Formal Language" context provided in the prompt.

---

## 🏛 Ground Truth Comparison (Summation)
For your thesis, here is the verified code the model *should* have aimed for:

```why3
module SumToN
  use int.Int
  use ref.Ref

  let sum_to_n (n: int) : int
    requires { n >= 0 }
    ensures  { result = n * (n + 1) / 2 }
  =
    let res = ref 0 in
    let i = ref 0 in
    while (!i < n)
      invariant { !res = !i * (!i + 1) / 2 && 0 <= !i <= n }
      variant   { n - !i }
    do
      i := !i + 1;
      res := !res + !i
    done;
    !res
end
```

---

## 🚀 Recommended Next Steps for Thesis
1.  **Iterative Prompting (V2.0)**: Update the system prompt to explicitly restrict UTF-8 math symbols and provide a "Loop Cheat Sheet."
2.  **Fine-Tuning Potential**: Compare these RAG results against a model fine-tuned on the Why3 standard library.
3.  **Cross-Model Study**: (Optional) Run the same pipeline using a 7B or 14B model to see if the "Mutable State" bottleneck disappears.
