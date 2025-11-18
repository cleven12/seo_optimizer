from typing import Dict, List
from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.scoring import ModuleResult, get_status

class StructureAnalyzer(BaseAnalyzer):
    def analyze(self) -> ModuleResult:
        score = 0
        details = {}
        recommendations = []
        
        h1_score, h1_details, h1_recs = self._analyze_h1()
        score += h1_score
        details['h1'] = h1_details
        recommendations.extend(h1_recs)
        
        hierarchy_score, hierarchy_details = self._analyze_heading_hierarchy()
        score += hierarchy_score
        details['heading_hierarchy'] = hierarchy_details
        
        img_score, img_details, img_recs = self._analyze_images()
        score += img_score
        details['images'] = img_details
        recommendations.extend(img_recs)
        
        score += 35
        
        return ModuleResult(
            module_name='Structure',
            score=min(100, score),
            status=get_status(min(100, score)),
            details=details,
            recommendations=recommendations
        )
    
    def _analyze_h1(self):
        h1_count = len(self.content.headings.get('h1', []))
        
        details = {
            'count': h1_count,
            'proper': h1_count == 1
        }
        
        recs = []
        if h1_count == 0:
            recs.append('Add an H1 heading to the page')
            score = 0
        elif h1_count == 1:
            score = 30
        else:
            recs.append(f'Use only one H1 heading (found {h1_count})')
            score = 15
        
        return score, details, recs
    
    def _analyze_heading_hierarchy(self):
        structure = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            count = len(self.content.headings.get(tag, []))
            for _ in range(count):
                structure.append(tag)
        
        details = {
            'proper': True,
            'structure': structure
        }
        
        score = 25
        
        return score, details
    
    def _analyze_images(self):
        total = len(self.content.images)
        with_alt = sum(1 for img in self.content.images if img['has_alt'])
        without_alt = total - with_alt
        
        details = {
            'total': total,
            'with_alt': with_alt,
            'without_alt': without_alt
        }
        
        recs = []
        if without_alt > 0:
            recs.append(f'Add alt text to {without_alt} image(s)')
            score = max(0, 15 - (without_alt * 3))
        else:
            score = 15
        
        return score, details, recs
