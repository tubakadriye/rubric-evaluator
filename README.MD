# Rubric Evaluation & Improvement System

## Overview

This project builds an automated system to **evaluate and improve grading rubrics** using LLMs and statistical metrics.

The system analyzes how well a rubric performs across three key goals:

1. **Ambiguity** → Do different graders produce consistent results?
2. **Applicability** → Does the rubric cover all valid answer types?
3. **Discrimination** → Does the rubric clearly separate strong and weak answers?

---
## Key Idea

The system follows a closed-loop evaluation process:

1. Simulate grading using LLMs (multiple runs, multiple models)
2. Measure statistical properties of grading behavior
3. Detect rubric weaknesses
4. Automatically generate an improved rubric


## Architecture

```
                ┌──────────────────────┐
                │   Input PDFs         │
                │ (Rubric, Students,   │
                │  Teaching Material)  │
                └─────────┬────────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
  Rubric Extractor   Student Answer   Teaching Extractor
                     Extractor   
          │               │                │
          └───────────────┴────────────────┘
                          │
                          ▼
          LLM Grading Simulation (Async, Multi-model)
                          │
                          ▼
                 Multi-run Evaluation
                          │
                          ▼
            ┌──────────────────────────────────┐
            │ Metrics Computation              │
            │ - Ambiguity (ICC)                │
            │ - Discrimination (Spearman)      │
            │ - Applicability (Edge Stability) │
            └──────────────────────────────────┘
                          │
                          ▼
                 Failure Detection
                          │
                          ▼
                 Rubric Improvement (LLM)
                          │
                          ▼
                    Human Review
```

---

## Approach

### 1. Data Extraction

- **Rubric** → extracted from PDF (PyMuPDF)
- **Student answers** → transcribed using multimodal LLM
- **Teaching material** → structured extraction via LLM

---

### 2. Grading Simulation

- Answers are graded using LLMs under the rubric
- Multiple runs simulate **independent graders**
- Multiple models (OpenAI + Claude) simulate **model disagreement**

This produces:
- repeated grading distributions
- cross-model differences

---

### 3. Synthetic Dataset 

To robustly evaluate the rubric, synthetic answers are generated:

- **Good answers** → correct, complete
- **Bad answers** → incorrect or missing key concepts
- **Edge cases** → partially correct / ambiguous

This enables controlled evaluation of:
- ranking behavior (discrimination)
- robustness (applicability)

---

### 4. Evaluation Metrics

#### 4.1 Ambiguity → Intraclass Correlation (ICC)

Measures **inter-rater reliability** across grading runs.

- Input: repeated grades per student
- High ICC → strong agreement → low ambiguity
- Low ICC → rubric interpretation is inconsistent

---

#### 4.2 Discrimination → Spearman Correlation

Measures whether ranking is preserved:

```
good > edge > bad 
```

- Input: scores + ordinal labels
- High correlation → rubric separates quality levels correctly

---

#### 4.3 Applicability → Edge Stability

Measures how the rubric behaves on ambiguous answers.

- Input: scores of edge-case answers
- High variance → rubric unstable / underspecified
- Very low variance → rubric overly rigid

The score is normalized relative to overall grading variability.

---

#### 4.4 Consistency

Measures variability across repeated grading runs.

- Based on standard deviation of scores
- Complements ICC (distribution-level vs agreement-level)

---

#### 4.5 Cross-model Consistency

Measures agreement between different LLMs (e.g. OpenAI vs Claude).

- Captures **model-dependent ambiguity**
- Important for robustness across evaluators

---

### 5. Rubric Improvement

The system combines:

- statistical signals (metrics)
- rubric analysis
- grading outputs

to generate an improved rubric that:

- reduces ambiguity
- improves coverage
- strengthens discrimination

---

### 6. Human Review

A human expert reviews the generated rubric via a simple CLI prompt  
(approve or edit before final output).

---

## Installation

```bash
brew install poppler
pip install -r requirements.txt
```

Set API keys:

```bash
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key
```

---

## Input Data

Place your input files in a data/ folder:

- Rubric PDF
- Teaching material PDF
- Student answer PDFs

The `data/` folder is excluded from version control via `.gitignore`.

### Run the Application

```bash
python -m app.main \
  --rubric data/ExamQuestionAndRubric.pdf \
  --teaching data/TeachingResource-BAD_ACTORS_STRATEGY.pdf \
  --students data/StudentAnswer-Student1.pdf data/StudentAnswer-Student2.pdf data/StudentAnswer-Student3.pdf
```

---

### Example Inputs

* `data/ExamQuestionAndRubric.pdf`
* `data/StudentAnswer-Student1.pdf`
* `data/TeachingResource.pdf`

---

## Output Format

```json
{
  "improved_rubric": {},
  "explanation": {
    "ambiguity": "...",
    "applicability": "...",
    "discrimination": "..."
  }
}
```

The result is also saved to:

```bash
output.json
```


---

## Key Insight

The system treats a rubric as a **measurable object**, not just text.

By combining:

* simulation (LLM grading)
* controlled data (synthetic answers)
* evaluation metrics

we can systematically improve rubric quality.

---

## Future Work

- Incorporate human-reviewed and labeled student answers to create a gold-standard evaluation set
- Extend evaluation beyond synthetic data to real-world exam responses
- Improve metric calibration using annotated datasets


