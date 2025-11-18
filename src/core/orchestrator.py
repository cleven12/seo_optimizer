from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from src.core.fetcher import fetch_content, WebContent
from src.core.keyword_processor import process_keywords, KeywordVariation
from src.analyzers.technical_seo import TechnicalSEOAnalyzer
from src.analyzers.content_analyzer import ContentAnalyzer, ClusterScore
from src.analyzers.structure_analyzer import StructureAnalyzer
from src.analyzers.link_analyzer import LinkAnalyzer
from src.core.scoring import calculate_overall_score, ModuleResult

@dataclass
class AnalysisReport:
    url: str
    analyzed_at: str
    overall_score: int
    keyword_cluster: ClusterScore
    technical_seo: ModuleResult
    content_analysis: ModuleResult
    structure_analysis: ModuleResult
    link_analysis: ModuleResult
    top_recommendations: List[str]

def run_analysis(url: str, keywords: List[str], verbose: bool = False) -> AnalysisReport:
    content = fetch_content(url)
    
    keyword_variations = process_keywords(keywords)
    
    technical_analyzer = TechnicalSEOAnalyzer(content, keyword_variations)
    technical_result = technical_analyzer.analyze()
    
    content_analyzer = ContentAnalyzer(content, keyword_variations)
    content_result = content_analyzer.analyze()
    
    structure_analyzer = StructureAnalyzer(content, keyword_variations)
    structure_result = structure_analyzer.analyze()
    
    link_analyzer = LinkAnalyzer(content, keyword_variations)
    link_result = link_analyzer.analyze()
    
    keyword_cluster = content_result.details['keyword_cluster']
    
    overall_score = calculate_overall_score(
        keyword_score=keyword_cluster.cluster_score,
        technical_score=technical_result.score,
        content_score=content_result.score,
        structure_score=structure_result.score,
        link_score=link_result.score
    )
    
    module_recommendations = []
    
    kw_recs = []
    for kw_score in keyword_cluster.individual_scores:
        kw_recs.extend([(kw_score.score, rec) for rec in kw_score.recommendations[:1]])
    kw_recs.sort(key=lambda x: x[0])
    module_recommendations.append(('keyword', kw_recs[:2]))
    
    tech_recs = [(technical_result.score, rec) for rec in technical_result.recommendations[:2]]
    module_recommendations.append(('technical', tech_recs))
    
    content_recs = [(content_result.score, rec) for rec in content_result.recommendations[:2]]
    module_recommendations.append(('content', content_recs))
    
    structure_recs = [(structure_result.score, rec) for rec in structure_result.recommendations[:2]]
    module_recommendations.append(('structure', structure_recs))
    
    link_recs = [(link_result.score, rec) for rec in link_result.recommendations[:2]]
    module_recommendations.append(('links', link_recs))
    
    all_recommendations = []
    for module_name, recs in module_recommendations:
        for score, rec in recs:
            all_recommendations.append((module_name, score, rec))
    
    all_recommendations.sort(key=lambda x: x[1])
    
    top_recommendations = [rec[2] for rec in all_recommendations[:8]]
    
    report = AnalysisReport(
        url=url,
        analyzed_at=datetime.now().isoformat(),
        overall_score=overall_score,
        keyword_cluster=keyword_cluster,
        technical_seo=technical_result,
        content_analysis=content_result,
        structure_analysis=structure_result,
        link_analysis=link_result,
        top_recommendations=top_recommendations
    )
    
    return report
