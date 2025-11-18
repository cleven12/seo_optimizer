from typing import Dict, List
from dataclasses import dataclass
from src.config import SCORE_WEIGHTS, KEYWORD_SCORE_WEIGHTS

@dataclass
class ModuleResult:
    module_name: str
    score: int
    status: str
    details: Dict
    recommendations: List[str]

def calculate_overall_score(
    keyword_score: int,
    technical_score: int,
    content_score: int,
    structure_score: int,
    link_score: int
) -> int:
    overall = (
        keyword_score * SCORE_WEIGHTS['keyword_analysis'] +
        technical_score * SCORE_WEIGHTS['technical_seo'] +
        content_score * SCORE_WEIGHTS['content_analysis'] +
        structure_score * SCORE_WEIGHTS['structure'] +
        link_score * SCORE_WEIGHTS['links']
    )
    
    return min(100, max(0, int(overall)))

def calculate_keyword_score(
    in_title: bool,
    in_meta: bool,
    in_h1: bool,
    in_headings: int,
    in_first_100_words: bool,
    density_score: float,
    distribution_score: float
) -> int:
    score = (
        (100 if in_title else 0) * KEYWORD_SCORE_WEIGHTS['title_match'] +
        (100 if in_meta else 0) * KEYWORD_SCORE_WEIGHTS['meta_match'] +
        (100 if in_h1 else 0) * KEYWORD_SCORE_WEIGHTS['h1_match'] +
        min(100, in_headings * 50) * KEYWORD_SCORE_WEIGHTS['headings_match'] +
        (100 if in_first_100_words else 0) * KEYWORD_SCORE_WEIGHTS['first_100_words'] +
        density_score * KEYWORD_SCORE_WEIGHTS['density_score'] +
        distribution_score * KEYWORD_SCORE_WEIGHTS['distribution_score']
    )
    
    return min(100, max(0, int(score)))

def get_status(score: int) -> str:
    if score >= 80:
        return 'passed'
    elif score >= 60:
        return 'warning'
    else:
        return 'failed'
