# Rubric Evaluation & Improvement System

## Overview

This project builds an automated pipeline to **evaluate and improve grading rubrics** using LLMs.

The system analyzes how well a rubric performs across three key goals:

1. **Ambiguity** → Do different graders produce consistent results?
2. **Applicability** → Does the rubric cover all valid answer types?
3. **Discrimination** → Does the rubric clearly separate strong and weak answers?

---

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
  Rubric Extractor   Student Answer Extractor   Teaching Extractor
          │               │                │
          └───────────────┴────────────────┘
                          │
                          ▼
                 Grading Simulation (LLM)
                          │
                          ▼
                 Multi-run Evaluation
                          │
                          ▼
        ┌──────────────────────────────────┐
        │ Metrics Computation              │
        │ - Ambiguity                     │
        │ - Discrimination                │
        │ - Applicability                 │
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

* Rubric extracted from PDF using PyMuPDF
* Student answers extracted via OCR / vision model
* Teaching material structured using multimodal LLM

---

### 2. Grading Simulation

* LLM grades answers using the rubric
* Multiple runs simulate different graders

---

### 3. Evaluation Metrics

#### Ambiguity

Measures grading consistency across runs
→ Based on **criterion-level disagreement**

#### Discrimination

Measures ranking quality:

```
good answers > edge cases > bad answers
```

#### Applicability

Measures:

* coverage of rubric criteria
* handling of edge cases

---

### 4. Synthetic Dataset (Optional but Recommended)

Synthetic answers are generated to:

* create controlled **good / bad / edge cases**
* evaluate discrimination and applicability

Optional human validation can be added to:

* define expected score ranges
* improve reliability

---

### 5. Rubric Improvement

The system:

* analyzes rubric weaknesses
* detects failures
* proposes an improved rubric using LLM reasoning

---

## Installation

```bash
brew install poppler
pip install -r requirements.txt
```

Set API key:

```bash
export OPENAI_API_KEY=your_key_here
```

---

## Run the Application

```bash
python -m app.main \
  --rubric data/rubric.pdf \
  --teaching data/teaching.pdf \
  --students data/s1.pdf data/s2.pdf
```

---

## Example Inputs

* `data/ExamQuestionAndRubric.pdf`
* `data/StudentAnswer-Student1.pdf`
* `data/TeachingResource.pdf`

---

## Output Format

```json
{
  "evaluation": {...},
  "improved_rubric": "...",
  "explanation": {...}
}
```

---

## Key Insight

The system treats a rubric as a **measurable object**, not just text.

By combining:

* simulation (LLM grading)
* controlled data (synthetic answers)
* evaluation metrics

we can **systematically improve rubric quality**.

---

## Future Improvements

* Human-in-the-loop calibration scoring
* Multi-model grading comparison
* Dataset expansion with real student answers
* Benchmarking across different rubric styles

---
