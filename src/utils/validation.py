import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """Validate if URL has proper scheme and network location."""
    try:
        if not isinstance(url, str):
            return False
        result = urlparse(url)
        return bool(result.scheme and result.netloc)
    except (TypeError, ValueError):
        return False

def validate_keywords(keywords: str) -> list:
    """Parse and validate comma-separated keywords."""
    if not keywords or not keywords.strip():
        raise ValueError("Keywords cannot be empty")
    
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
    
    if not keyword_list:
        raise ValueError("No valid keywords provided")
    
    if len(keyword_list) > 50:
        raise ValueError("Too many keywords (max 50)")
    
    return keyword_list
