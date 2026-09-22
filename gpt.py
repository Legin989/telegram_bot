import json
import logging

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AsyncOpenAI,
    RateLimitError,
)

from config import settings
from utils import load_prompt

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=settings.OPENAI_TIMEOUT
)

FALLBACK = "😔 Не вдалося звʼязатися з ChatGPT. Спробуй ще раз за хвилину."


async def send_request_ai(message: str) -> str:
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system","content": load_prompt("gpt")},
                {"role": "user","content": message}
            ],
            reasoning_effort=settings.OPENAI_REASONING,
            max_completion_tokens=settings.OPENAI_MAX_TOKENS
        )
    except Exception as e:
        logger.error(e)
        return FALLBACK


    print(response)

    return response.choices[0].message.content or ""