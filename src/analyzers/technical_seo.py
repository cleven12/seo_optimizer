from typing import Dict, List
from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.scoring import ModuleResult, get_status
from src.config import OPTIMAL_TITLE_LENGTH_MIN, OPTIMAL_TITLE_LENGTH_MAX, OPTIMAL_META_DESC_LENGTH_MIN, OPTIMAL_META_DESC_LENGTH_MAX

class TechnicalSEOAnalyzer(BaseAnalyzer):
    def analyze(self) -> ModuleResult:
        score = 0
        details = {}
        recommendations = []
        
        title_score, title_details, title_recs = self._analyze_title()
        score += title_score
        details['title'] = title_details
        recommendations.extend(title_recs)
        
        meta_score, meta_details, meta_recs = self._analyze_meta_description()
        score += meta_score
        details['meta_description'] = meta_details
        recommendations.extend(meta_recs)
        
        canonical_score, canonical_details = self._analyze_canonical()
        score += canonical_score
        details['canonical'] = canonical_details
        
        og_score, og_details = self._analyze_open_graph()
        score += og_score
        details['open_graph'] = og_details
        
        details['http_status'] = 200
        score += 10
        
        return ModuleResult(
            module_name='Technical SEO',
            score=min(100, score),
            status=get_status(min(100, score)),
            details=details,
            recommendations=recommendations
        )
    
    def _analyze_title(self):
        score = 0
        recs = []
        
        if not self.content.title:
            return 0, {'present': False}, ['Add a title tag']
        
        title_len = len(self.content.title)
        optimal = OPTIMAL_TITLE_LENGTH_MIN <= title_len <= OPTIMAL_TITLE_LENGTH_MAX
        
        details = {
            'present': True,
            'length': title_len,
            'optimal_length': optimal,
            'content': self.content.title
        }
        
        if self.content.title:
            score += 15
            if optimal:
                score += 15
            else:
                if title_len < OPTIMAL_TITLE_LENGTH_MIN:
                    recs.append(f'Title is too short ({title_len} chars), aim for {OPTIMAL_TITLE_LENGTH_MIN}-{OPTIMAL_TITLE_LENGTH_MAX}')
                else:
                    recs.append(f'Title is too long ({title_len} chars), aim for {OPTIMAL_TITLE_LENGTH_MIN}-{OPTIMAL_TITLE_LENGTH_MAX}')
        
        return score, details, recs
    
    def _analyze_meta_description(self):
        score = 0
        recs = []
        
        if not self.content.meta_description:
            return 0, {'present': False}, ['Add a meta description']
        
        meta_len = len(self.content.meta_description)
        optimal = OPTIMAL_META_DESC_LENGTH_MIN <= meta_len <= OPTIMAL_META_DESC_LENGTH_MAX
        
        details = {
            'present': True,
            'length': meta_len,
            'optimal_length': optimal,
            'content': self.content.meta_description
        }
        
        if self.content.meta_description:
            score += 12
            if optimal:
                score += 13
            else:
                if meta_len < OPTIMAL_META_DESC_LENGTH_MIN:
                    recs.append(f'Meta description too short ({meta_len} chars), aim for {OPTIMAL_META_DESC_LENGTH_MIN}-{OPTIMAL_META_DESC_LENGTH_MAX}')
                else:
                    recs.append(f'Meta description too long ({meta_len} chars), aim for {OPTIMAL_META_DESC_LENGTH_MIN}-{OPTIMAL_META_DESC_LENGTH_MAX}')
        
        return score, details, recs
    
    def _analyze_canonical(self):
        canonical = self.content.soup.find('link', rel='canonical')
        
        details = {
            'present': bool(canonical),
            'url': canonical.get('href', '') if canonical else None
        }
        
        score = 10 if canonical else 0
        
        return score, details
    
    def _analyze_open_graph(self):
        og_title = self.content.soup.find('meta', property='og:title')
        og_desc = self.content.soup.find('meta', property='og:description')
        
        present = bool(og_title or og_desc)
        complete = bool(og_title and og_desc)
        
        details = {
            'present': present,
            'complete': complete
        }
        
        score = 15 if complete else (7 if present else 0)
        
        return score, details
