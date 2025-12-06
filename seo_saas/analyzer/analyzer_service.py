"""Service module for running SEO analysis and generating reports."""

import sys
from pathlib import Path
import time
from typing import List, Dict, Any, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.core.orchestrator import run_analysis as run_cli_analysis
from src.config import (
    KEYWORD_SCORE_WEIGHTS,
    CLUSTER_KEYWORD_SCORE_WEIGHTS,
    SEO_SCORE_THRESHOLDS
)


def run_seo_analysis(
    url: str,
    keywords: Optional[List[str]] = None,
    use_ai: bool = False,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Run comprehensive SEO analysis on a URL.
    
    Args:
        url: Target URL to analyze
        keywords: Optional list of keywords to focus on
        use_ai: Whether to include AI recommendations
        verbose: Verbose output
    
    Returns:
        Dictionary with analysis results
    """
    try:
        # If no keywords provided, use page title or default keywords
        if not keywords:
            from src.core.fetcher import fetch_content
            try:
                content = fetch_content(url)
                # Extract keywords from title
                title = content.title or ""
                if title:
                    # Split title into meaningful keywords
                    keywords = [word.strip() for word in title.split() if len(word.strip()) > 3][:3]
                else:
                    keywords = ["seo", "optimization"]
            except:
                keywords = ["seo", "optimization"]
        
        # Run the CLI analysis orchestrator
        report = run_cli_analysis(url, keywords, verbose, use_ai)
        
        # Transform the report into API format
        return transform_analysis_report(report)
    
    except Exception as e:
        raise Exception(f"Analysis failed: {str(e)}")


def transform_analysis_report(report) -> Dict[str, Any]:
    """
    Transform CLI analysis report to API format.
    
    Args:
        report: AnalysisReport from orchestrator
    
    Returns:
        Formatted analysis result
    """
    def _to_primitive(obj):
        """Convert common analysis dataclass objects into primitives recursively.

        This helper supports the specific data models returned by the analyzer
        (ClusterScore, KeywordScore and nested structures) and falls back to
        converting objects via __dict__ or repr string for unknown types.
        """
        # Primitives
        if obj is None or isinstance(obj, (str, bool, int, float)):
            return obj
        # Dates & datetimes
        import datetime as _dt
        if isinstance(obj, (_dt.datetime, _dt.date)):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)
        if isinstance(obj, list):
            return [_to_primitive(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _to_primitive(v) for k, v in obj.items()}

        # Known analyzer objects
        if hasattr(obj, 'keyword') and hasattr(obj, 'score'):
            return {
                'keyword': getattr(obj, 'keyword', None),
                'score': getattr(obj, 'score', None)
            }

        if hasattr(obj, 'cluster_score') and hasattr(obj, 'keywords'):
            result = {
                'keywords': getattr(obj, 'keywords', None),
                'cluster_score': getattr(obj, 'cluster_score', None)
            }
            if hasattr(obj, 'individual_scores'):
                result['individual_scores'] = _to_primitive(getattr(obj, 'individual_scores'))
            return result

        # Fallback to introspecting attrs
        try:
            attrs = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
            return {k: _to_primitive(v) for k, v in attrs.items()}
        except Exception:
            return str(obj)

    # Extract scores
    overall_score = report.overall_score
    
    scores = {
        'technical': report.technical_seo.score if report.technical_seo else 0,
        'content': report.content_analysis.score if report.content_analysis else 0,
        'structure': report.structure_analysis.score if report.structure_analysis else 0,
        'links': report.link_analysis.score if report.link_analysis else 0,
    }
    
    # Extract recommendations
    recommendations = report.top_recommendations if report.top_recommendations else []
    
    # Extract keywords and their scores
    keywords_data = []
    if hasattr(report, 'keyword_cluster') and report.keyword_cluster:
        keyword_cluster = report.keyword_cluster
        # keyword_cluster is a ClusterScore object with individual_scores list
        if hasattr(keyword_cluster, 'individual_scores'):
            for kw_score in keyword_cluster.individual_scores:
                keywords_data.append({
                    'keyword': kw_score.keyword,
                    'score': kw_score.score,
                })
        # Also add the main keywords if available
        if hasattr(keyword_cluster, 'keywords'):
            # Get cluster score
            cluster_score_val = keyword_cluster.cluster_score if hasattr(keyword_cluster, 'cluster_score') else 0
            keywords_data.insert(0, {
                'keyword': ', '.join(keyword_cluster.keywords) if keyword_cluster.keywords else 'Main Keywords',
                'score': cluster_score_val,
            })
    
    # Build analysis details
    technical_details = {}
    if report.technical_seo:
        technical_details = {
            'score': report.technical_seo.score,
            'status': report.technical_seo.status,
            'details': _to_primitive(report.technical_seo.details or {}),
            'recommendations': report.technical_seo.recommendations or [],
        }
    
    content_details = {}
    if report.content_analysis:
        content_details = {
            'score': report.content_analysis.score,
            'status': report.content_analysis.status,
            'details': _to_primitive(report.content_analysis.details or {}),
            'recommendations': report.content_analysis.recommendations or [],
        }
    
    structure_details = {}
    if report.structure_analysis:
        structure_details = {
            'score': report.structure_analysis.score,
            'status': report.structure_analysis.status,
            'details': _to_primitive(report.structure_analysis.details or {}),
            'recommendations': report.structure_analysis.recommendations or [],
        }
    
    link_details = {}
    if report.link_analysis:
        link_details = {
            'score': report.link_analysis.score,
            'status': report.link_analysis.status,
            'details': _to_primitive(report.link_analysis.details or {}),
            'recommendations': report.link_analysis.recommendations or [],
        }
    
    ai_recommendations = []
    if hasattr(report, 'ai_analysis') and report.ai_analysis:
        ai_recommendations = report.ai_analysis.recommendations or []
    
    result = {
        'url': report.url,
        'title': getattr(report, 'title', ''),
        'overall_score': overall_score,
        'scores': scores,
        'keywords': keywords_data,
        'recommendations': recommendations,
        'analysis_data': {
            'analyzed_at': report.analyzed_at,
        },
        'technical_details': technical_details,
        'content_details': content_details,
        'structure_details': structure_details,
        'link_details': link_details,
        'ai_recommendations': ai_recommendations,
    }

    # Ensure entire response is JSON-friendly (no dataclasses or objects)
    return _to_primitive(result)


def generate_pdf_report(report_obj) -> bytes:
    """
    Generate professional PDF report from analysis.
    
    Args:
        report_obj: AnalysisReport model instance
    
    Returns:
        PDF content as bytes
    """
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )
    
    # Collect story elements
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=12,
    )
    
    # Title
    story.append(Paragraph('SEO Analysis Report', title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # URL and Score
    score_color = get_score_color(report_obj.overall_score)
    score_paragraph = Paragraph(
        f'<b>Website:</b> {report_obj.url}<br/>'
        f'<b>Overall Score:</b> <font color="{score_color}"><b>{report_obj.overall_score}/100</b></font><br/>'
        f'<b>Analysis Date:</b> {report_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")}<br/>',
        styles['Normal']
    )
    story.append(score_paragraph)
    story.append(Spacer(1, 0.3*inch))
    
    # Score Breakdown
    story.append(Paragraph('Score Breakdown', heading_style))
    
    score_data = [
        ['Category', 'Score', 'Status'],
        ['Technical SEO', f'{report_obj.technical_score}/100', get_status_label(report_obj.technical_score)],
        ['Content Quality', f'{report_obj.content_score}/100', get_status_label(report_obj.content_score)],
        ['Structure & Markup', f'{report_obj.structure_score}/100', get_status_label(report_obj.structure_score)],
        ['Link Quality', f'{report_obj.link_score}/100', get_status_label(report_obj.link_score)],
    ]
    
    score_table = Table(score_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Keywords (if any)
    if report_obj.keywords:
        story.append(Paragraph('Analyzed Keywords', heading_style))
        keywords_text = ', '.join(report_obj.keywords) if isinstance(report_obj.keywords, list) else str(report_obj.keywords)
        story.append(Paragraph(f'<b>Keywords:</b> {keywords_text}', styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
    
    # Top Recommendations
    if report_obj.recommendations:
        story.append(Paragraph('Top Recommendations', heading_style))
        
        recommendations = report_obj.recommendations if isinstance(report_obj.recommendations, list) else []
        for i, rec in enumerate(recommendations[:10], 1):
            rec_text = rec if isinstance(rec, str) else str(rec)
            story.append(Paragraph(
                f'<b>{i}.</b> {rec_text}',
                styles['Normal']
            ))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Analysis Details
    try:
        if hasattr(report_obj, 'details') and report_obj.details:
            details = report_obj.details
            
            # Technical SEO Details
            if details.technical_details:
                story.append(PageBreak())
                story.append(Paragraph('Technical SEO Details', heading_style))
                
                tech_details = details.technical_details
                for key, value in tech_details.items():
                    if key != 'recommendations':
                        story.append(Paragraph(
                            f'<b>{key.replace("_", " ").title()}:</b> {str(value)[:200]}',
                            styles['Normal']
                        ))
                        story.append(Spacer(1, 0.08*inch))
            
            # Content Details
            if details.content_details:
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph('Content Quality Details', heading_style))
                
                content_details = details.content_details
                for key, value in content_details.items():
                    if key != 'recommendations':
                        story.append(Paragraph(
                            f'<b>{key.replace("_", " ").title()}:</b> {str(value)[:200]}',
                            styles['Normal']
                        ))
                        story.append(Spacer(1, 0.08*inch))
    except:
        pass
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = (
        '<b>SEO Optimizer Report</b><br/>'
        'For more information and guidelines, visit the SEO Optimizer documentation.<br/>'
        f'Generated on {report_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    )
    story.append(Paragraph(footer_text, ParagraphStyle(
        'footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
    )))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content


def get_score_color(score: int) -> str:
    """Get color based on score."""
    if score >= 80:
        return '#10b981'  # Green
    elif score >= 60:
        return '#f59e0b'  # Orange
    elif score >= 40:
        return '#ef4444'  # Red
    else:
        return '#7f1d1d'  # Dark Red


def get_status_label(score: int) -> str:
    """Get status label based on score."""
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Fair'
    else:
        return 'Poor'
