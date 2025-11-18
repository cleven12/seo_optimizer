import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_keywords(keywords: str) -> list:
    if not keywords or not keywords.strip():
        raise ValueError("Keywords cannot be empty")
    
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
    
    if not keyword_list:
        raise ValueError("No valid keywords provided")
    
    return keyword_list
