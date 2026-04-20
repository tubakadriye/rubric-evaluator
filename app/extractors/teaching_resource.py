import fitz
import base64
from openai import OpenAI

client = OpenAI()


# ----------------------------
# 1. Convert PDF → images
# ----------------------------
def pdf_to_base64_images(pdf_path: str):
    doc = fitz.open(pdf_path)
    images = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        base64_img = base64.b64encode(img_bytes).decode("utf-8")

        images.append({
            "type": "input_image",
            "image_url": f"data:image/png;base64,{base64_img}",
            "detail": "high"
        })

    return images


# ----------------------------
# 2. Extract structured content
# ----------------------------
def extract_teaching_material(pdf_path: str):

    images = pdf_to_base64_images(pdf_path)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": """
You are extracting teaching material from a PDF.

IMPORTANT:
- Do NOT summarize.
- Extract EVERYTHING visible.
- Preserve structure exactly.
- Include diagram content (WENN diagrams, arrows, boxes).
- If text is in a figure, transcribe it.
- If relationships exist, describe them explicitly.

OUTPUT FORMAT (strict JSON):

{
  "key_concepts": [],
  "definitions": [],
  "diagram_explanations": [],
  "relationships": [],
  "raw_notes": []
}

Rules:
- Be exhaustive
- Do not omit small details
- Do not interpret beyond visible information
"""
                },
                *images
            ]
        }]
    )

    extracted_text = response.output_text

    return extracted_text