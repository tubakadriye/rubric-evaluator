from openai import OpenAI
import fitz
import base64
import json
import os

client = OpenAI()


def pdf_to_images(pdf_path, dpi=200):
    doc = fitz.open(pdf_path)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        images.append(f"data:image/png;base64,{b64}")

    return images

def extract_student_transcription_raw(pdf_paths, output_file="student_transcriptions.json"):
    results = []

    for path in pdf_paths:
        images = pdf_to_images(path)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
You are a transcription system for handwritten exam answers.

IMPORTANT:
- Do NOT summarize
- Do NOT interpret
- Do NOT improve grammar
- Preserve structure
- Use [unclear] if needed

Return STRICT JSON:

{
  "transcription": "...",
  "uncertain_words": [],
  "confidence": 0-100
}
"""
                    },
                    *[
                        {
                            "type": "input_image",
                            "image_url": img,
                            "detail": "high"
                        }
                        for img in images
                    ]
                ]
            }]
        )

        raw_output = response.output_text

        try:
            parsed = json.loads(raw_output)
        except:
            parsed = {
                "transcription": raw_output,
                "uncertain_words": [],
                "confidence": 0
            }

        results.append({
            "file": path,
            "result": parsed
        })

    # 💾 SAVE TO FILE
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


def extract_student_transcription(pdf_paths):
    results = []

    for item in extract_student_transcription_raw(pdf_paths):
        results.append(item["result"]["transcription"])

    return results