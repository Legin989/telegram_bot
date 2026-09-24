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


async def ask(system_prompt: str, user_message: str) -> str | None:
    messages=[
        {"role": "system","content": system_prompt},
        {"role": "user","content": user_message}
    ]
    return await complate(messages)

async def ask_history(system_prompt: str, history: list[dict[str, str]]) -> str | None:
    messages=[
        {"role": "system",
         "content": system_prompt},
        *history
    ]



async def complate(message: list[dict[str,str]]) ->list[str] | str | None:
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=message,
            reasoning_effort=settings.OPENAI_REASONING,
            max_completion_tokens=settings.OPENAI_MAX_TOKENS
        )
    except RateLimitError as e:
        logger.error(
            "Забагато спроб"
        )
        return None
    except APITimeoutError as e:
        logger.error(
            "Сервер OpenAI не відповіда"
        )
        return None
    except APIConnectionError as e:
        logger.error(
            "Не вийшло з'єднатись з OpenAI, зачекайте"
        )
        return None
    except APIStatusError as e:
        logger.error(
            "Трапилась помилка"
        )
        return None
    except Exception as e:
        logger.error(e)
        return None

    content = response.choices[0].message.content or ""

    if not content:
        logger.warning("Повернув порожню відповідь")
        return None


    if len(content) > 4096:
        result = []

        while content:
             part = content[:4096]
             content = content[4096:]
             result.append(part)

        return result
    return content