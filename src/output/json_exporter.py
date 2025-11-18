import json
from dataclasses import asdict
from src.core.orchestrator import AnalysisReport

def export_to_json(report: AnalysisReport, filepath: str):
    report_dict = {
        'meta': {
            'url': report.url,
            'analyzed_at': report.analyzed_at,
            'keywords_analyzed': report.keyword_cluster.keywords
        },
        'overall_score': report.overall_score,
        'keyword_analysis': {
            'cluster_score': report.keyword_cluster.cluster_score,
            'individual_keywords': [
                {
                    'keyword': ks.keyword,
                    'score': ks.score,
                    'findings': ks.findings,
                    'recommendations': ks.recommendations
                }
                for ks in report.keyword_cluster.individual_scores
            ]
        },
        'technical_seo': {
            'score': report.technical_seo.score,
            'status': report.technical_seo.status,
            'details': report.technical_seo.details,
            'recommendations': report.technical_seo.recommendations
        },
        'content_analysis': {
            'score': report.content_analysis.score,
            'status': report.content_analysis.status,
            'details': {
                'word_count': report.content_analysis.details['word_count'],
                'adequate_length': report.content_analysis.details['adequate_length']
            },
            'recommendations': report.content_analysis.recommendations
        },
        'structure_analysis': {
            'score': report.structure_analysis.score,
            'status': report.structure_analysis.status,
            'details': report.structure_analysis.details,
            'recommendations': report.structure_analysis.recommendations
        },
        'link_analysis': {
            'score': report.link_analysis.score,
            'status': report.link_analysis.status,
            'details': report.link_analysis.details,
            'recommendations': report.link_analysis.recommendations
        },
        'top_recommendations': report.top_recommendations
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report_dict, f, indent=2, ensure_ascii=False)
