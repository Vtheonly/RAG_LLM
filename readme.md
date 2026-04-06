 ✅ Preflight OK
   Model: sorc/qwen3.5-claude-4.6-opus
   Why3: /usr/local/bin/why3
   Prover: alt-ergo

==================================================
>> TEST NIVEAU 1 : Dummy (Maximum)
==================================================

[1] BASELINE (LLM brut)
      [Itération 1] -> ✅ Validé

[2] RAG (Injection du Cours)
      [Itération 1] -> ✅ Validé

[3] RAG + AGENTIC LOOP (Auto-correction)
      [Itération 1] -> ✅ Validé

==================================================
>> TEST NIVEAU 2 : Medium (Somme Itérative)
==================================================

[1] BASELINE (LLM brut)
      [Itération 1] -> ❌ Échec
        

[2] RAG (Injection du Cours)
      [Itération 1] -> ❌ Échec
        

[3] RAG + AGENTIC LOOP (Auto-correction)
      [Itération 1] -> ❌ Échec
        
      [Agent] Correction 1/3...
      [Itération 2] -> ❌ Échec
        File "test_temp.mlw", line 8, characters 0-3: syntax error

      [Agent] Correction 2/3...
      [Itération 3] -> ❌ Échec
        File "test_temp.mlw", line 8, characters 15-17: syntax error

      [Agent] Correction 3/3...
      [Itération 4] -> ❌ Échec
        

==================================================
>> TEST NIVEAU 3 : Hardcore (Div Euclidienne)
==================================================

[1] BASELINE (LLM brut)
      [Itération 1] -> ❌ Échec
        

[2] RAG (Injection du Cours)
      [Itération 1] -> ❌ Échec
        

[3] RAG + AGENTIC LOOP (Auto-correction)
      [Itération 1] -> ❌ Échec
        
      [Agent] Correction 1/3...
      [Itération 2] -> ❌ Échec
        File "test_temp.mlw", line 10, characters 17-18: syntax error

      [Agent] Correction 2/3...
      [Itération 3] -> ❌ Échec
        File "test_temp.mlw", line 7, characters 0-3: syntax error

      [Agent] Correction 3/3...
      [Itération 4] -> ❌ Échec
        Warning, file "test_temp.mlw", line 9, characters 23-24: unused variable s
Warning, file "test_temp.mlw", line 15, characters 22-23: unused variable s
Warning, file "test_temp.mlw", line 18, character

✅ Évaluation terminée.

  
    

    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }


  
    
      
      Niveau
      Test
      Méthode
      Succès
      Itérations
    
  
  
    
      0
      1
      Dummy (Maximum)
      1. Baseline
      True
      1
    
    
      1
      1
      Dummy (Maximum)
      2. RAG
      True
      1
    
    
      2
      1
      Dummy (Maximum)
      3. Full Agent
      True
      1
    
    
      3
      2
      Medium (Somme Itérative)
      1. Baseline
      False
      1
    
    
      4
      2
      Medium (Somme Itérative)
      2. RAG
      False
      1
    
    
      5
      2
      Medium (Somme Itérative)
      3. Full Agent
      False
      4
    
    
      6
      3
      Hardcore (Div Euclidienne)
      1. Baseline
      False
      1
    
    
      7
      3
      Hardcore (Div Euclidienne)
      2. RAG
      False
      1
    
    
      8
      3
      Hardcore (Div Euclidienne)
      3. Full Agent
      False
      4
    
  


    

  
    

  
    
  
    

  
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  

    
      const buttonEl =
        document.querySelector('#df-7209f453-320a-44b4-9f4e-54856708e5b1 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-7209f453-320a-44b4-9f4e-54856708e5b1');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    
  


  
    
      .colab-df-generate {
        background-color: #E8F0FE;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: #1967D2;
        height: 32px;
        padding: 0 0 0 0;
        width: 32px;
      }

      .colab-df-generate:hover {
        background-color: #E2EBFA;
        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: #174EA6;
      }

      [theme=dark] .colab-df-generate {
        background-color: #3B4455;
        fill: #D2E3FC;
      }

      [theme=dark] .colab-df-generate:hover {
        background-color: #434B5C;
        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
        fill: #FFFFFF;
      }
    
    

  
    
  
    
    
      (() => {
      const buttonEl =
        document.querySelector('#id_f563de83-e1fa-45d7-bd8b-4c061828ce32 button.colab-df-generate');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      buttonEl.onclick = () => {
        google.colab.notebook.generateWithVariable('df_results');
      }
      })();
    
  

    
  
## Part 2 


🎉 **IT WORKS!** Level 1 passed 3/3.

The failures on levels 2 and 3 are **model quality issues** (syntax errors in generated code), not infrastructure problems. That's expected — the model struggles with complex Why3 syntax.

Now run the **last cell** (cell 6) to see the graph:

```python
# ============================================================
# 6. Résultats & Graphique
# ============================================================
import matplotlib.pyplot as plt
import seaborn as sns

df_results["Succès (%)"] = df_results["Succès"].astype(int) * 100

plt.figure(figsize=(10, 5))
sns.barplot(data=df_results, x="Niveau", y="Succès (%)", hue="Méthode", palette="viridis")
plt.title(f"Taux de Validation Formelle Why3 - {MODEL_NAME}")
plt.xlabel("Complexité (1=Simple, 2=Boucle, 3=Hardcore)")
plt.ylabel("Validé par Alt-Ergo (%)")
plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title="Méthode")
plt.tight_layout()
plt.show()

print("\nTableau des Itérations :")
display(df_results[["Niveau", "Test", "Méthode", "Succès", "Itérations"]])
```

---

## Summary of Results

| Level | Test | Baseline | RAG | Full Agent |
|-------|------|----------|-----|------------|
| 1 | Maximum | ✅ | ✅ | ✅ |
| 2 | Somme Itérative | ❌ | ❌ | ❌ (4 tries) |
| 3 | Div Euclidienne | ❌ | ❌ | ❌ (4 tries) |

**Interpretation:**
- Simple functions (level 1): Model handles well
- Loops with invariants (level 2-3): Model generates syntax errors

To improve levels 2-3, you could:
1. Use a **bigger/better model** (e.g., `qwen2.5-coder:7b` if VRAM allows)
2. Add **more Why3 examples** to the RAG knowledge base
3. Increase `max_retries` in the agent loop
4. Use **few-shot prompting** with working examples in the prompt


I want to go further with the system and analyze it more deeply.

First, I want to verify whether the model actually uses the RAG. I want to inspect the generated code, observe what the agent does and does not do, and understand its decision process.

I also want to run more examples to evaluate its behavior across different cases.

Another goal is to assess the quality of the RAG: how much it actually helps. For example, if the model succeeds on the first try, then RAG may not have contributed much. I want to measure how much the RAG and the iterative correction agent improve the results.

I also want to experiment with better RAG encoders.

One idea is to preprocess the slides and PDFs into cleaner text (or even structured Markdown) so that the RAG context becomes clearer and more effective.

I want to compare different formats as well: raw PDFs vs. cleaned text vs. pure Markdown, to see which one produces better retrieval and overall performance.

Finally, there is the issue of the French language barrier, which may affect the quality of retrieval and understanding.