from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.cache import cached_call, cache_key
import logging

client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)


def call_llm(prompt, model, temperature=0.0):

    key = cache_key(f"{model}:{temperature}:{prompt}")

    def run():
        try:
            res = client.responses.create(
                model=model,
                input=prompt,
                temperature=temperature
            )
            return res.output_text
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return ""

    return cached_call(key, run)