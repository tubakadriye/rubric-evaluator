from app.llm.client import call_llm
from app.utils.json_utils import extract_json
from app.config import MODEL_GRADING

def improve_rubric(prompt):
    out = call_llm(prompt, MODEL_GRADING, temperature= 0.4)
    return extract_json(out)