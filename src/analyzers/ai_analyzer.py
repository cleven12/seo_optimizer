import os
import json
from typing import Dict, List, Optional
from anthropic import Anthropic
from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.scoring import ModuleResult, get_status

# The newest Anthropic model is "claude-sonnet-4-20250514", not "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022" nor "claude-3-sonnet-20240229". 
# Always prefer using "claude-sonnet-4-20250514" as it is the latest model.
DEFAULT_MODEL = "claude-sonnet-4-20250514"

class AIAnalyzer(BaseAnalyzer):
    def __init__(self, content, keyword_variations, current_scores: Dict):
        super().__init__(content, keyword_variations)
        self.current_scores = current_scores
        self.client = None
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key:
            self.client = Anthropic(api_key=api_key)
    
    def analyze(self) -> ModuleResult:
        if not self.client:
            return ModuleResult(
                module_name='AI SEO Assistant',
                score=0,
                status='failed',
                details={'error': 'ANTHROPIC_API_KEY not configured'},
                recommendations=['Add ANTHROPIC_API_KEY to enable AI-powered SEO suggestions']
            )
        
        try:
            ai_recommendations = self._generate_ai_recommendations()
            optimized_title = self._generate_optimized_title()
            optimized_meta = self._generate_optimized_meta_description()
            content_suggestions = self._analyze_content_quality()
            
            details = {
                'ai_recommendations': ai_recommendations,
                'optimized_title': optimized_title,
                'optimized_meta_description': optimized_meta,
                'content_quality_analysis': content_suggestions,
                'model_used': DEFAULT_MODEL
            }
            
            recommendations = ai_recommendations[:3] if ai_recommendations else []
            
            return ModuleResult(
                module_name='AI SEO Assistant',
                score=100,
                status='passed',
                details=details,
                recommendations=recommendations
            )
        
        except Exception as e:
            return ModuleResult(
                module_name='AI SEO Assistant',
                score=0,
                status='failed',
                details={'error': str(e)},
                recommendations=[f'AI analysis failed: {str(e)}']
            )
    
    def _generate_ai_recommendations(self) -> List[str]:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        
        prompt = f"""Analyze this webpage SEO and provide 5 specific, actionable recommendations.

URL: {self.content.url}
Target Keywords: {keywords}
Title: {self.content.title or 'Missing'}
Meta Description: {self.content.meta_description or 'Missing'}
H1: {self.content.h1 or 'Missing'}
Word Count: {self.content.word_count}
Current SEO Scores:
- Technical SEO: {self.current_scores.get('technical', 0)}/100
- Content: {self.current_scores.get('content', 0)}/100
- Structure: {self.current_scores.get('structure', 0)}/100
- Links: {self.current_scores.get('links', 0)}/100

Body Text Preview: {self.content.body_text[:500]}...

Provide exactly 5 specific, actionable SEO recommendations. Format as a JSON array of strings.
Focus on the biggest impact improvements based on the scores."""
        
        response = self.client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        try:
            recommendations = json.loads(content)
            if isinstance(recommendations, list):
                return recommendations[:5]
        except:
            lines = [line.strip() for line in content.strip().split('\n') if line.strip() and not line.strip().startswith('[') and not line.strip().startswith(']')]
            return [line.lstrip('0123456789.- ') for line in lines if line][:5]
        
        return []
    
    def _generate_optimized_title(self) -> Optional[str]:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        current_title = self.content.title or ''
        
        prompt = f"""Generate an SEO-optimized title tag for this webpage.

Target Keywords: {keywords}
Current Title: {current_title}
Page Content: {self.content.body_text[:300]}...

Requirements:
- 50-60 characters long
- Include primary keyword naturally
- Compelling and click-worthy
- Accurate to page content

Provide ONLY the optimized title, nothing else."""
        
        try:
            response = self.client.messages.create(
                model=DEFAULT_MODEL,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            
            title = response.content[0].text.strip().strip('"\'')
            return title if 40 <= len(title) <= 70 else None
        except:
            return None
    
    def _generate_optimized_meta_description(self) -> Optional[str]:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        current_meta = self.content.meta_description or ''
        
        prompt = f"""Generate an SEO-optimized meta description for this webpage.

Target Keywords: {keywords}
Current Meta: {current_meta}
Page Content: {self.content.body_text[:400]}...

Requirements:
- 150-160 characters long
- Include primary keyword naturally
- Compelling call-to-action
- Accurate summary of page content

Provide ONLY the optimized meta description, nothing else."""
        
        try:
            response = self.client.messages.create(
                model=DEFAULT_MODEL,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            meta = response.content[0].text.strip().strip('"\'')
            return meta if 120 <= len(meta) <= 180 else None
        except:
            return None
    
    def _analyze_content_quality(self) -> Dict:
        prompt = f"""Analyze the SEO content quality of this text.

Content: {self.content.body_text[:800]}...

Evaluate:
1. Readability level (1-10)
2. Engagement potential (1-10)
3. Keyword stuffing risk (1-10, higher = more risk)
4. Content value (1-10)

Respond in JSON format:
{{"readability": number, "engagement": number, "keyword_stuffing_risk": number, "content_value": number, "summary": "brief summary"}}"""
        
        try:
            response = self.client.messages.create(
                model=DEFAULT_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            
            try:
                return json.loads(content)
            except:
                if 'readability' in content.lower():
                    return {'summary': 'Content quality analysis completed', 'readability': 7}
                return {'summary': 'Unable to parse quality metrics'}
        except:
            return {'summary': 'Analysis failed'}
