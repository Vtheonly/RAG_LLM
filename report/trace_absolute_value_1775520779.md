# Trace Log: Absolute Value

## Instruction
Écris une fonction `let abs (x: int) : int` qui retourne la valeur absolue de x. Ajoute ensures { result >= 0 } et ensures { result = x \/ result = -x }.

## RAG Context Retrieved
```text
--- SOURCE: /content/RAG_LLM/llm_formal_verification/les_md_cours/4.md (Page Unknown Page) ---
### Fichier 20 : Cours 5 - Exemples d'application de règles (Tant-que)
```markdown
# Cours 5 : Exemple d'application (Boucle)
**Auteur :** A. Giorgetti
**Pages / Diapositives :** 165 à 166

## Exemple : `while (k < n)`
Invariant de boucle `I` : `k = i ∧ k ≤ n`
Programme `p` : `{i = i + 1; k = k + 1;}`
Variables modifiées `V` : `i := i1, k := k1`

1. **Condition initiale :** `i = 0 ⇒ {k := 0} I`
2. **Préservation :** `i = 0 ⇒ {k := 0, i := i1, k := k1} ((I ∧ k < n) → [p] I)`
3. **Sortie :** `i = 0 ⇒ {k := 0, i := i1, k := k1} ((I ∧ ¬(k < n)) → (i = n))`

* Une fois la 3ème condition réduite par arithmétique et substitution, on conclut par transitivité et symétrie de l'égalité.
```

### Fichier 21 : Cours 4 - Règles de clôture dans KeY
```markdown
# Cours 4 : Clôture de sous-buts (Fol / Sequent Calculus)
**Auteur :** A. Giorgetti
**Pages / Diapositives :** 142 à 144

## Conditions de clôture (Proof Branch Closed)
Une branche de preuve peut être fermée si :
1. **Séquent valide :** 
   - `Γ, φ ⇒ φ, Δ` (close)
   - `Γ ⇒ true, Δ` (true)
   - `Γ, false ⇒ Δ` (false)
2. **Équation évidente :** `Γ ⇒ t = t, Δ` (eqClose)

--- SOURCE: /content/RAG_LLM/llm_formal_verification/les_md_cours/1.md (Page Unknown Page) ---
## Système de règles d'inférence (Sémantique axiomatique)
Le système déductif repose sur plusieurs règles permettant de prouver la validité des triplets de Hoare :

### 1. Règle pour l'affectation
```text
{P (e/x)} x := e {P}    (assignment)

C'est un axiome (il n'y a pas de prémisse).

(e/x) formalise la substitution uniforme de la variable x par l'expression e dans la formule P.

L'affectation x := e donne la valeur de e à x. Donc P (portant sur x) est vraie après l'affectation si P(e/x) était vraie avant.

2. Règle pour la composition séquentielle
code
Text
download
content_copy
expand_less
{P} c {Q}      {Q} c' {R}
------------------------------ (sequence)
        {P} c; c' {R}

Pour dériver {P} c; c' {R}, il faut deviner une formule intermédiaire Q.

Q agit comme une notion d'assertion pour documenter le programme.

Le calcul de Q amène à la notion de plus faible précondition.

3. Règle pour l'instruction conditionnelle (if-then-else)
code
Text
download
content_copy
expand_less
{b ∧ P} c1 {Q}      {¬b ∧ P} c2 {Q}
------------------------------------------ (if-then-else)
    {P} if b then c1 else c2 fi {Q}

L'expression booléenne b est considérée comme une formule portant sur les variables d'état.

Si b n'est pas une formule stricte, on la remplace par b = true et ¬b par b = false.

--- SOURCE: /content/RAG_LLM/llm_formal_verification/les_md_cours/3.md (Page Unknown Page) ---
### Fichier 18 : Cours 4 - Sémantique et Calcul des Séquents
```markdown
# Cours 4 : Sémantique et Calcul des séquents
**Auteur :** A. Giorgetti
**Pages / Diapositives :** 109 à 144

## Sémantique
* L'interprétation nécessite une signature, un domaine (univers typé `D`), et une fonction d'interprétation `I`.
* La validité (`|= φ`) est vraie si la formule est vraie dans tous les modèles (états).

## Calcul des Séquents
Utilisé pour prouver la validité de manière syntaxique (sans énumérer les modèles) :
`Γ =⇒ Δ`
* **Axiomes :** `Γ, φ =⇒ φ, Δ` est toujours valide.
* **Règles :** Permettent de transformer les formules (`andRight`, `orLeft`, `allRight`, etc.).
* **Soundness & Completeness :** Le système est correct (si une preuve close existe, la formule est valide) et complet (si une formule est valide, une preuve close existe).
* **Preuve de `∃` ou `∀` :** Nécessite des règles d'instanciation (souvent avec des constantes "nouvelles" pour `allRight` ou des termes témoins pour `exRight`).
```
```

## Attempt 1
**Prompt passed to LLM:**
```text
You are an expert formal verification engineer specializing in Why3 and MLW syntax.
You will be provided with context from a university course on formal methods (in French).
Your task is to write valid, mathematically sound Why3 code to solve the user's prompt.

### WHY3 SYNTAX CHEAT SHEET ###
module Example
  use int.Int
  use ref.Ref

  let function_name (x: int) : int
    requires { x >= 0 }
    ensures  { result = x + 1 }
  =
    x + 1
end

### CRITICAL INSTRUCTIONS ###
1. Output ONLY the code inside a ```why3 ... ``` block.
2. Do NOT write any conversational text, greetings, or explanations.
3. ALWAYS include 'module', 'requires', 'ensures', and if using loops, 'invariant' and 'variant'.
4. Module names MUST start with a Capital letter (e.g. `module MaxFunction`, not `module max`).
5. NEVER leave precondition brackets empty like `requires {}`. Use `requires { true }` instead.
6. MANDATORY ATTRIBUTION: You MUST include a comment at the top of your code citing the PDF source and page number from the provided context (e.g., `(* Derived from: Course01, Page 12 *)`).
7. GROUNDING: If you use a specific invariant or library from the context, mention it in a comment.

COURSE CONTEXT (RAG):
--- SOURCE: /content/RAG_LLM/llm_formal_verification/les_md_cours/4.md (Page Unknown Page) ---
### Fichier 20 : Cours 5 - Exemples d'application de règles (Tant-que)
```markdown
# Cours 5 : Exemple d'application (Boucle)
**Auteur :** A. Giorgetti
**Pages / Diapositives :** 165 à 166

## Exemple : `while (k < n)`
Invariant de boucle `I` : `k = i ∧ k ≤ n`
Programme `p` : `{i = i + 1; k = k + 1;}`
Variables modifiées `V` : `i := i1, k := k1`

1. **Condition initiale :** `i = 0 ⇒ {k := 0} I`
2. **Préservation :** `i = 0 ⇒ {k := 0, i := i1, k := k1} ((I ∧ k < n) → [p] I)`
3. **Sortie :** `i = 0 ⇒ {k := 0, i := i1, k := k1} ((I ∧ ¬(k < n)) → (i = n))`

* Une fois la 3ème condition réduite par arithmétique et substitution, on conclut par transitivité et symétrie de l'égalité.
```

### Fichier 21 : Cours 4 - Règles de clôture dans KeY
```markdown
# Cours 4 : Clôture de sous-buts (Fol / Sequent Calculus)
**Auteur :** A. Giorgetti
**Pages / Diapositives :** 142 à 144

## Conditions de clôture (Proof Branch Closed)
Une branche de preuve peut être fermée si :
1. **Séquent valide :** 
   - `Γ, φ ⇒ φ, Δ` (close)
   - `Γ ⇒ true, Δ` (true)
   - `Γ, false ⇒ Δ` (false)
2. **Équation évidente :** `Γ ⇒ t = t, Δ` (eqClose)

--- SOURCE: /content/RAG_LLM/llm_formal_verification/les_md_cours/1.md (Page Unknown Page) ---
## Système de règles d'inférence (Sémantique axiomatique)
Le système déductif repose sur plusieurs règles permettant de prouver la validité des triplets de Hoare :

### 1. Règle pour l'affectation
```text
{P (e/x)} x := e {P}    (assignment)

C'est un axiome (il n'y a pas de prémisse).

(e/x) formalise la substitution uniforme de la variable x par l'expression e dans la formule P.

L'affectation x := e donne la valeur de e à x. Donc P (portant sur x) est vraie après l'affectation si P(e/x) était vraie avant.

2. Règle pour la composition séquentielle
code
Text
download
content_copy
expand_less
{P} c {Q}      {Q} c' {R}
------------------------------ (sequence)
        {P} c; c' {R}

Pour dériver {P} c; c' {R}, il faut deviner une formule intermédiaire Q.

Q agit comme une notion d'assertion pour documenter le programme.

Le calcul de Q amène à la notion de plus faible précondition.

3. Règle pour l'instruction conditionnelle (if-then-else)
code
Text
download
content_copy
expand_less
{b ∧ P} c1 {Q}      {¬b ∧ P} c2 {Q}
------------------------------------------ (if-then-else)
    {P} if b then c1 else c2 fi {Q}

L'expression booléenne b est considérée comme une formule portant sur les variables d'état.

Si b n'est pas une formule stricte, on la remplace par b = true et ¬b par b = false.

--- SOURCE: /content/RAG_LLM/llm_formal_verification/les_md_cours/3.md (Page Unknown Page) ---
### Fichier 18 : Cours 4 - Sémantique et Calcul des Séquents
```markdown
# Cours 4 : Sémantique et Calcul des séquents
**Auteur :** A. Giorgetti
**Pages / Diapositives :** 109 à 144

## Sémantique
* L'interprétation nécessite une signature, un domaine (univers typé `D`), et une fonction d'interprétation `I`.
* La validité (`|= φ`) est vraie si la formule est vraie dans tous les modèles (états).

## Calcul des Séquents
Utilisé pour prouver la validité de manière syntaxique (sans énumérer les modèles) :
`Γ =⇒ Δ`
* **Axiomes :** `Γ, φ =⇒ φ, Δ` est toujours valide.
* **Règles :** Permettent de transformer les formules (`andRight`, `orLeft`, `allRight`, etc.).
* **Soundness & Completeness :** Le système est correct (si une preuve close existe, la formule est valide) et complet (si une formule est valide, une preuve close existe).
* **Preuve de `∃` ou `∀` :** Nécessite des règles d'instanciation (souvent avec des constantes "nouvelles" pour `allRight` ou des termes témoins pour `exRight`).
```

USER INSTRUCTION:
Écris une fonction `let abs (x: int) : int` qui retourne la valeur absolue de x. Ajoute ensures { result >= 0 } et ensures { result = x \/ result = -x }.
```

**LLM Generated Code:**
```why3
(* Derived from: Cours 4, Page Unknown Page *)
module AbsFunction
  use int.Int

  let abs (x: int) : int
    requires { true } (* Aucune précondition spécifique nécessaire pour la valeur absolue *)
    ensures { result >= 0 }
    ensures { result = x \/ result = -x }
  =
    if x >= 0 then
      x
    else
      -x
end
```

**Why3 Feedback (Valid: True):**
```text
File /content/RAG_LLM/llm_formal_verification/test_temp.mlw:
Goal abs'vc.
Prover result is: Valid (0.02s, 7 steps).


```

