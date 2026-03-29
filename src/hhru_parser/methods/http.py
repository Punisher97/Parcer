import asyncio
from typing import Optional

import httpx

from hhru_parser.methods.base import BaseParser

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


class HTTPParser(BaseParser):
    def __init__(
        self,
        client: httpx.AsyncClient,
        retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        self.client = client
        self.retries = retries
        self.retry_delay = retry_delay

    async def fetch_text(self, url: str) -> str:
        last_error: Exception| None = None

        for attempt in range(1, self.retries + 1):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.text

            except httpx.HTTPStatusError as error:
                last_error = error
                status_code = error.response.status_code

                if status_code in (403, 404):
                    raise

                if status_code == 429 and attempt < self.retries:
                    await asyncio.sleep(self.retry_delay * attempt)
                    continue

                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay * attempt)
                    continue

            except httpx.RequestError as error:
                last_error = error
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay * attempt)
                    continue

        if last_error is not None:
            raise last_error

        raise RuntimeError("Unexpected HTTP fetch error")


async def create_async_client(timeout: float = 15.0) -> httpx.AsyncClient:
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
    return httpx.AsyncClient(
        headers=DEFAULT_HEADERS,
        timeout=timeout,
        follow_redirects=True,
        limits=limits,
    )
