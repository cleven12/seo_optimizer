from typing import List, Dict
from dataclasses import dataclass
from src.utils.text_utils import normalize_text, tokenize, remove_stop_words, stem_words, stem_word

@dataclass
class KeywordVariation:
    original: str
    stemmed: str
    variations: List[str]
    stop_words_removed: str

def process_keyword(keyword: str) -> KeywordVariation:
    original = keyword.strip()
    normalized = normalize_text(original)
    
    words = tokenize(normalized)
    words_no_stop = remove_stop_words(words)
    stop_words_removed = ' '.join(words_no_stop)
    
    stemmed_words = stem_words(words_no_stop)
    stemmed = ' '.join(stemmed_words)
    
    variations = [
        normalized,
        stop_words_removed,
        stemmed
    ]
    
    return KeywordVariation(
        original=original,
        stemmed=stemmed,
        variations=list(set(variations)),
        stop_words_removed=stop_words_removed
    )

def match_keyword_in_text(keyword_variation: KeywordVariation, text: str) -> bool:
    if not text:
        return False
    
    text_normalized = normalize_text(text)
    
    if keyword_variation.original.lower() in text_normalized:
        return True
    
    if keyword_variation.stop_words_removed and keyword_variation.stop_words_removed in text_normalized:
        return True
    
    text_words = tokenize(text_normalized)
    text_stemmed_words = stem_words(text_words)
    text_stemmed = ' '.join(text_stemmed_words)
    
    if keyword_variation.stemmed and keyword_variation.stemmed in text_stemmed:
        return True
    
    return False

def process_keywords(keywords: List[str]) -> List[KeywordVariation]:
    return [process_keyword(kw) for kw in keywords]
