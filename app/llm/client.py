from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.utils.cache import cached_call, cache_key
import logging
from openai import AsyncOpenAI
import time

async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)


def normalize(text):
    return " ".join(text.split())


def call_llm(prompt, model, temperature=0.0, retries=3):

    key = cache_key(f"{model}:{temperature}:{normalize(prompt)}")

    def run():
        for i in range(retries):
            try:
                res = client.responses.create(
                    model=model,
                    input=prompt,
                    temperature=temperature
                )
                return getattr(res, "output_text", "")
            except Exception as e:
                logger.warning(f"Retry {i+1}: {e}")
                time.sleep(1.5 * (i+1))

        raise RuntimeError("LLM failed after retries")

    return cached_call(key, run)