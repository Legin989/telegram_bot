import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
        OPEN_API_KEY: str = os.getenv("OPEN_API_KEY", "")
        BOT_API_KEY: str = os.getenv("BOT_API_KEY", "")
        OPEN_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5-6-luna")
        OPENAI_REASONING: str = os.getenv("OPENAI_REASONING", "none")
        OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "600"))
        OPENAI_TIMEOUT : float = float(os.getenv("OPENAI_TIMEOUT", "30"))

settings = Settings()