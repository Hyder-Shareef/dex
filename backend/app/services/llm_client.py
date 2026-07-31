from openai import OpenAI

from app.config import settings

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if not settings.llm_api_key:
        raise RuntimeError("LLM_API_KEY is not configured.")
    if _client is None:
        kwargs = {"api_key": settings.llm_api_key}
        if settings.llm_base_url:
            kwargs["base_url"] = settings.llm_base_url
        _client = OpenAI(**kwargs)
    return _client
