from typing import Dict, List
from dataclasses import dataclass
from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.keyword_processor import match_keyword_in_text, KeywordVariation
from src.core.scoring import calculate_keyword_score, get_status, ModuleResult
from src.utils.text_utils import calculate_density, get_first_n_words
from src.config import OPTIMAL_KEYWORD_DENSITY_MIN, OPTIMAL_KEYWORD_DENSITY_MAX, MIN_WORD_COUNT

@dataclass
class KeywordScore:
    keyword: str
    score: int
    in_title: bool
    in_meta: bool
    in_h1: bool
    in_headings: List[str]
    in_first_100_words: bool
    density: float
    distribution_score: int
    findings: Dict
    recommendations: List[str]

@dataclass
class ClusterScore:
    keywords: List[str]
    cluster_score: int
    individual_scores: List[KeywordScore]

class ContentAnalyzer(BaseAnalyzer):
    def analyze(self) -> ModuleResult:
        individual_scores = []
        
        for kw_var in self.keyword_variations:
            kw_score = self._analyze_keyword(kw_var)
            individual_scores.append(kw_score)
        
        avg_score = sum(ks.score for ks in individual_scores) / len(individual_scores) if individual_scores else 0
        
        cluster = ClusterScore(
            keywords=[kw.original for kw in self.keyword_variations],
            cluster_score=int(avg_score),
            individual_scores=individual_scores
        )
        
        word_count_adequate = self.content.word_count >= MIN_WORD_COUNT
        
        word_count_score = 0
        recommendations = []
        
        if word_count_adequate:
            word_count_score = 50
        else:
            word_count_score = (self.content.word_count / MIN_WORD_COUNT) * 50
            recommendations.append(f'Increase content length to at least {MIN_WORD_COUNT} words (currently {self.content.word_count})')
        
        avg_density = sum(ks.density for ks in individual_scores) / len(individual_scores) if individual_scores else 0
        density_health_score = 0
        if OPTIMAL_KEYWORD_DENSITY_MIN <= avg_density <= OPTIMAL_KEYWORD_DENSITY_MAX:
            density_health_score = 50
        elif avg_density < OPTIMAL_KEYWORD_DENSITY_MIN:
            density_health_score = (avg_density / OPTIMAL_KEYWORD_DENSITY_MIN) * 50
            recommendations.append(f'Improve keyword density (currently {avg_density:.1f}%)')
        else:
            density_health_score = max(0, 50 - (avg_density - OPTIMAL_KEYWORD_DENSITY_MAX) * 10)
            recommendations.append(f'Reduce keyword density to avoid keyword stuffing (currently {avg_density:.1f}%)')
        
        content_score = int(word_count_score + density_health_score)
        
        details = {
            'word_count': self.content.word_count,
            'adequate_length': word_count_adequate,
            'avg_keyword_density': avg_density,
            'keyword_cluster': cluster
        }
        
        return ModuleResult(
            module_name='Content Analysis',
            score=content_score,
            status=get_status(content_score),
            details=details,
            recommendations=recommendations
        )
    
    def _analyze_keyword(self, kw_var: KeywordVariation) -> KeywordScore:
        in_title = match_keyword_in_text(kw_var, self.content.title or '')
        in_meta = match_keyword_in_text(kw_var, self.content.meta_description or '')
        in_h1 = match_keyword_in_text(kw_var, self.content.h1 or '')
        
        in_headings = []
        for tag, headings in self.content.headings.items():
            for heading in headings:
                if match_keyword_in_text(kw_var, heading):
                    in_headings.append(tag)
                    break
        
        first_100 = get_first_n_words(self.content.body_text, 100)
        in_first_100_words = match_keyword_in_text(kw_var, first_100)
        
        density = calculate_density(kw_var.original, self.content.body_text)
        
        if OPTIMAL_KEYWORD_DENSITY_MIN <= density <= OPTIMAL_KEYWORD_DENSITY_MAX:
            density_score = 100
        elif density < OPTIMAL_KEYWORD_DENSITY_MIN:
            density_score = (density / OPTIMAL_KEYWORD_DENSITY_MIN) * 100
        else:
            density_score = max(0, 100 - (density - OPTIMAL_KEYWORD_DENSITY_MAX) * 20)
        
        distribution_score = 70
        
        score = calculate_keyword_score(
            in_title=in_title,
            in_meta=in_meta,
            in_h1=in_h1,
            in_headings=len(in_headings),
            in_first_100_words=in_first_100_words,
            density_score=density_score,
            distribution_score=distribution_score
        )
        
        recommendations = []
        if not in_title:
            recommendations.append(f"Add '{kw_var.original}' to title tag")
        if not in_meta:
            recommendations.append(f"Add '{kw_var.original}' to meta description")
        if not in_h1:
            recommendations.append(f"Include '{kw_var.original}' in H1 heading")
        if density < OPTIMAL_KEYWORD_DENSITY_MIN:
            recommendations.append(f"Increase keyword density (currently {density:.1f}%)")
        
        return KeywordScore(
            keyword=kw_var.original,
            score=score,
            in_title=in_title,
            in_meta=in_meta,
            in_h1=in_h1,
            in_headings=in_headings,
            in_first_100_words=in_first_100_words,
            density=density,
            distribution_score=int(distribution_score),
            findings={
                'in_title': in_title,
                'in_meta': in_meta,
                'in_h1': in_h1,
                'in_headings': in_headings,
                'in_first_100_words': in_first_100_words,
                'density': density
            },
            recommendations=recommendations
        )
