from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    async def fetch_text(self, url: str) -> str:
        pass