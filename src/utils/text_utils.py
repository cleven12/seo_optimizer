import re
from typing import List
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stemmer = PorterStemmer()

def ensure_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

def normalize_text(text: str) -> str:
    return text.lower().strip()

def tokenize(text: str) -> List[str]:
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def remove_stop_words(words: List[str]) -> List[str]:
    ensure_nltk_data()
    stop_words = set(stopwords.words('english'))
    return [w for w in words if w not in stop_words]

def stem_word(word: str) -> str:
    return stemmer.stem(word.lower())

def stem_words(words: List[str]) -> List[str]:
    return [stem_word(w) for w in words]

def calculate_density(keyword: str, text: str) -> float:
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    words = tokenize(text)
    total_words = len(words)
    
    if total_words == 0:
        return 0.0
    
    keyword_words = tokenize(keyword_lower)
    keyword_count = 0
    
    if len(keyword_words) == 1:
        keyword_count = text_lower.count(keyword_lower)
    else:
        keyword_pattern = r'\b' + r'\s+'.join(keyword_words) + r'\b'
        keyword_count = len(re.findall(keyword_pattern, text_lower))
    
    return (keyword_count / total_words) * 100

def get_first_n_words(text: str, n: int) -> str:
    words = tokenize(text)
    return ' '.join(words[:n])
