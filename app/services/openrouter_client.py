import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    async def ask(
        self,
        messages: list[dict[str, str]],
        temperature: float,
    ) -> str:
        if not settings.openrouter_api_key:
            raise ExternalServiceError("OpenRouter API key is not configured")

        url = f"{settings.openrouter_base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                )

            response.raise_for_status()

        except httpx.HTTPStatusError as error:
            raise ExternalServiceError(
                f"OpenRouter returned error: {error.response.text}",
            ) from error

        except httpx.HTTPError as error:
            raise ExternalServiceError(
                "OpenRouter request failed",
            ) from error

        data = response.json()

        try:
            answer = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise ExternalServiceError(
                "Invalid OpenRouter response format",
            ) from error

        return str(answer)
