import os
import json
from typing import Dict, List, Optional
from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.scoring import ModuleResult, get_status

# Note: the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
# Note: the newest OpenAI model is "gpt-5" which was released August 7, 2025
# do not change these unless explicitly requested by the user

class AIAnalyzer(BaseAnalyzer):
    def __init__(self, content, keyword_variations, current_scores: Dict):
        super().__init__(content, keyword_variations)
        self.current_scores = current_scores
        self.client = None
        self.ai_type = None
        self.model = None
        
        gemini_key = os.environ.get('GEMINI_API_KEY')
        openai_key = os.environ.get('OPENAI_API_KEY')
        
        if gemini_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=gemini_key)
                self.ai_type = 'gemini'
                self.model = 'gemini-2.5-flash'
            except ImportError:
                pass
        
        if not self.client and openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=openai_key)
                self.ai_type = 'openai'
                self.model = 'gpt-5'
            except ImportError:
                pass
    
    def analyze(self) -> ModuleResult:
        if not self.client:
            return ModuleResult(
                module_name='AI SEO Assistant',
                score=0,
                status='failed',
                details={'error': 'No AI API key configured'},
                recommendations=['Add GEMINI_API_KEY (free) or OPENAI_API_KEY to enable AI-powered SEO suggestions']
            )
        
        try:
            ai_recommendations = self._generate_ai_recommendations()
            optimized_title = self._generate_optimized_title()
            optimized_meta = self._generate_optimized_meta_description()
            content_suggestions = self._analyze_content_quality()
            grammar_analysis = self._analyze_grammar_seo_safe()
            
            details = {
                'ai_recommendations': ai_recommendations,
                'optimized_title': optimized_title,
                'optimized_meta_description': optimized_meta,
                'content_quality_analysis': content_suggestions,
                'grammar_analysis': grammar_analysis,
                'model_used': self.model,
                'ai_provider': self.ai_type
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
        
        prompt = f"""Analyze this webpage SEO and provide 5 specific, actionable recommendations focused on the target keywords: {keywords}

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

Provide exactly 5 specific, actionable SEO recommendations specifically for the keywords: {keywords}
Focus on the biggest impact improvements based on the scores and keyword optimization.
Respond with JSON in this format: {{"recommendations": ["recommendation 1", "recommendation 2", ...]}}"""
        
        try:
            if self.ai_type == 'gemini':
                from google.genai import types
                from pydantic import BaseModel
                
                class Recommendations(BaseModel):
                    recommendations: List[str]
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are an SEO expert analyzing web pages for keyword optimization.",
                        response_mime_type="application/json",
                        response_schema=Recommendations,
                    )
                )
                
                result = json.loads(response.text)
                
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an SEO expert analyzing web pages for keyword optimization."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    max_completion_tokens=1024
                )
                
                result = json.loads(response.choices[0].message.content)
            
            if 'recommendations' in result and isinstance(result['recommendations'], list):
                return result['recommendations'][:5]
            
            return []
        except Exception as e:
            return [f"Unable to generate AI recommendations: {str(e)}"]
    
    def _generate_optimized_title(self) -> Optional[str]:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        current_title = self.content.title or ''
        
        prompt = f"""Generate an SEO-optimized title tag for this webpage that focuses on these keywords: {keywords}

Target Keywords: {keywords}
Current Title: {current_title}
Page Content: {self.content.body_text[:300]}...

Requirements:
- 50-60 characters long
- Include the primary keyword from the list: {keywords}
- Compelling and click-worthy
- Accurate to page content

Provide ONLY the optimized title, nothing else."""
        
        try:
            if self.ai_type == 'gemini':
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={'system_instruction': "You are an SEO expert. Generate only the title tag text, nothing else."}
                )
                title = response.text.strip().strip('"\'')
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an SEO expert. Generate only the title tag text, nothing else."},
                        {"role": "user", "content": prompt}
                    ],
                    max_completion_tokens=100
                )
                title = response.choices[0].message.content.strip().strip('"\'')
            
            return title if 40 <= len(title) <= 70 else None
        except:
            return None
    
    def _generate_optimized_meta_description(self) -> Optional[str]:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        current_meta = self.content.meta_description or ''
        
        prompt = f"""Generate an SEO-optimized meta description for this webpage that focuses on these keywords: {keywords}

Target Keywords: {keywords}
Current Meta: {current_meta}
Page Content: {self.content.body_text[:400]}...

Requirements:
- 150-160 characters long
- Include the primary keyword from: {keywords}
- Compelling call-to-action
- Accurate summary of page content

Provide ONLY the optimized meta description, nothing else."""
        
        try:
            if self.ai_type == 'gemini':
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={'system_instruction': "You are an SEO expert. Generate only the meta description text, nothing else."}
                )
                meta = response.text.strip().strip('"\'')
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an SEO expert. Generate only the meta description text, nothing else."},
                        {"role": "user", "content": prompt}
                    ],
                    max_completion_tokens=150
                )
                meta = response.choices[0].message.content.strip().strip('"\'')
            
            return meta if 120 <= len(meta) <= 180 else None
        except:
            return None
    
    def _analyze_content_quality(self) -> Dict:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        
        prompt = f"""Analyze the SEO content quality of this text for the keywords: {keywords}

Content: {self.content.body_text[:800]}...

Evaluate:
1. Readability level (1-10)
2. Engagement potential (1-10)
3. Keyword stuffing risk (1-10, higher = more risk)
4. Content value (1-10)
5. How well it targets the keywords: {keywords}

Respond in JSON format:
{{"readability": number, "engagement": number, "keyword_stuffing_risk": number, "content_value": number, "keyword_targeting": number, "summary": "brief summary"}}"""
        
        try:
            if self.ai_type == 'gemini':
                from google.genai import types
                from pydantic import BaseModel
                
                class ContentQuality(BaseModel):
                    readability: int
                    engagement: int
                    keyword_stuffing_risk: int
                    content_value: int
                    keyword_targeting: int
                    summary: str
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are an SEO content quality expert.",
                        response_mime_type="application/json",
                        response_schema=ContentQuality,
                    )
                )
                
                return json.loads(response.text)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an SEO content quality expert."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    max_completion_tokens=300
                )
                
                return json.loads(response.choices[0].message.content.strip())
        except:
            return {'summary': 'Analysis failed'}
    
    def _analyze_grammar_seo_safe(self) -> Dict:
        keywords = ', '.join([kw.original for kw in self.keyword_variations])
        
        title_text = self.content.title or ''
        meta_text = self.content.meta_description or ''
        h1_text = self.content.h1 or ''
        body_preview = self.content.body_text[:1000]
        
        prompt = f"""Analyze the grammar and readability of this SEO content. Identify grammar issues and suggest improvements WITHOUT changing or removing the target keywords: {keywords}

CRITICAL RULES:
- DO NOT remove or change the keywords: {keywords}
- Keep keyword density intact (preserve all keyword mentions)
- Only fix grammar, punctuation, and sentence structure
- Improve readability without affecting SEO

Title: {title_text}
Meta Description: {meta_text}
H1: {h1_text}
Body Content Preview: {body_preview}

Target Keywords to PRESERVE: {keywords}

Analyze and provide:
1. Overall grammar score (1-10, where 10 is perfect)
2. Number of grammar issues found
3. Top 3 grammar improvements (keep keywords intact)
4. Readability improvements (without keyword changes)

Respond in JSON format:
{{
  "grammar_score": number,
  "issues_found": number,
  "title_improvement": "improved title (if needed, preserve keywords)",
  "meta_improvement": "improved meta description (if needed, preserve keywords)",
  "grammar_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
  "readability_tips": ["tip 1", "tip 2"],
  "seo_preserved": true
}}"""
        
        try:
            if self.ai_type == 'gemini':
                from google.genai import types
                from pydantic import BaseModel
                
                class GrammarAnalysis(BaseModel):
                    grammar_score: int
                    issues_found: int
                    title_improvement: str
                    meta_improvement: str
                    grammar_suggestions: List[str]
                    readability_tips: List[str]
                    seo_preserved: bool
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are a grammar expert who understands SEO. Fix grammar WITHOUT removing keywords.",
                        response_mime_type="application/json",
                        response_schema=GrammarAnalysis,
                    )
                )
                
                return json.loads(response.text)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a grammar expert who understands SEO. Fix grammar WITHOUT removing keywords."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    max_completion_tokens=500
                )
                
                return json.loads(response.choices[0].message.content.strip())
        except:
            return {
                'grammar_score': 0,
                'issues_found': 0,
                'grammar_suggestions': [],
                'readability_tips': [],
                'seo_preserved': True,
                'error': 'Grammar analysis failed'
            }
