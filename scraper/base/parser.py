from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseParser(ABC):
    """
    Abstract base class for all content parsers.
    Defines the interface for parsing raw content into a structured format.
    """
    @abstractmethod
    async def parse(self, raw_content: Any, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Parses the raw content and extracts relevant information.
        
        Args:
            raw_content (Any): The raw content to parse (e.g., RSS feed dict, HTML string).
            **kwargs: Additional arguments for the parsing process.
            
        Returns:
            Optional[Dict[str, Any]]: A dictionary containing structured data (e.g., title, url),
                                     or None if parsing fails.
        """
        pass

    @abstractmethod
    async def parse_article_content(self, url: str, html_content: str, **kwargs) -> Optional[str]:
        """
        Parses the full article content from its dedicated HTML page.
        This is typically used if the summary in RSS is insufficient.
        
        Args:
            url (str): The URL of the article page.
            html_content (str): The raw HTML content of the article page.
            **kwargs: Additional arguments for the parsing process.
            
        Returns:
            Optional[str]: The extracted main article content as a string, or None if extraction fails.
        """
        pass
