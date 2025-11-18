OPTIMAL_KEYWORD_DENSITY_MIN = 1.0
OPTIMAL_KEYWORD_DENSITY_MAX = 3.0

OPTIMAL_TITLE_LENGTH_MIN = 50
OPTIMAL_TITLE_LENGTH_MAX = 60

OPTIMAL_META_DESC_LENGTH_MIN = 150
OPTIMAL_META_DESC_LENGTH_MAX = 160

RECOMMENDED_INTERNAL_LINKS_MIN = 5
RECOMMENDED_INTERNAL_LINKS_MAX = 10

MIN_WORD_COUNT = 300

REQUEST_TIMEOUT = 10
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

SCORE_WEIGHTS = {
    'keyword_analysis': 0.40,
    'technical_seo': 0.20,
    'content_analysis': 0.20,
    'structure': 0.10,
    'links': 0.10
}

KEYWORD_SCORE_WEIGHTS = {
    'title_match': 0.20,
    'meta_match': 0.15,
    'h1_match': 0.15,
    'headings_match': 0.10,
    'first_100_words': 0.10,
    'density_score': 0.15,
    'distribution_score': 0.15
}
