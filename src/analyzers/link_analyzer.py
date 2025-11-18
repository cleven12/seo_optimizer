from typing import Dict, List
from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.scoring import ModuleResult, get_status
from src.config import RECOMMENDED_INTERNAL_LINKS_MIN, RECOMMENDED_INTERNAL_LINKS_MAX

class LinkAnalyzer(BaseAnalyzer):
    def analyze(self) -> ModuleResult:
        score = 0
        details = {}
        recommendations = []
        
        internal_links = [link for link in self.content.links if link['is_internal']]
        external_links = [link for link in self.content.links if link['is_external']]
        
        internal_count = len(internal_links)
        external_count = len(external_links)
        
        if RECOMMENDED_INTERNAL_LINKS_MIN <= internal_count <= RECOMMENDED_INTERNAL_LINKS_MAX:
            internal_score = 35
        elif internal_count < RECOMMENDED_INTERNAL_LINKS_MIN:
            internal_score = (internal_count / RECOMMENDED_INTERNAL_LINKS_MIN) * 35
            needed = RECOMMENDED_INTERNAL_LINKS_MIN - internal_count
            recommendations.append(f'Add {needed} more internal link(s)')
        else:
            internal_score = 35
        
        score += int(internal_score)
        
        if external_count > 0:
            score += 25
        else:
            recommendations.append('Add some external links to authoritative sources')
        
        score += 25
        
        score += 15
        
        details['internal_links'] = {
            'count': internal_count,
            'recommended_min': RECOMMENDED_INTERNAL_LINKS_MIN
        }
        details['external_links'] = {
            'count': external_count
        }
        
        return ModuleResult(
            module_name='Links',
            score=min(100, score),
            status=get_status(min(100, score)),
            details=details,
            recommendations=recommendations
        )
