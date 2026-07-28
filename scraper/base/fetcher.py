from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseFetcher(ABC):
    """
    Abstract base class for all content fetchers.
    Defines the interface for fetching raw content from a given URL.
    """
    @abstractmethod
    async def fetch(self, url: str, **kwargs) -> Optional[Any]:
        """
        Fetches content from the specified URL.
        
        Args:
            url (str): The URL to fetch content from.
            **kwargs: Additional arguments for the fetching process (e.g., headers, timeout).
            
        Returns:
            Optional[Any]: The raw content (e.g., text, bytes) if successful, otherwise None.
        """
        pass
