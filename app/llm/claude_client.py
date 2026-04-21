from anthropic import Anthropic
from app.config import ANTHROPIC_API_KEY
import os

client = Anthropic(api_key= ANTHROPIC_API_KEY)

def call_claude(prompt):

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text