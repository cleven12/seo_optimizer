from abc import ABC, abstractmethod
from typing import Any, List
from src.core.fetcher import WebContent
from src.core.keyword_processor import KeywordVariation

class BaseAnalyzer(ABC):
    def __init__(self, content: WebContent, keyword_variations: List[KeywordVariation]):
        self.content = content
        self.keyword_variations = keyword_variations
    
    @abstractmethod
    def analyze(self) -> Any:
        pass
