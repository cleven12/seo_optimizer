from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.core.orchestrator import AnalysisReport

console = Console()

def render_report(report: AnalysisReport, verbose: bool = False):
    console.print()
    keywords_str = ', '.join([f'"{kw}"' for kw in report.keyword_cluster.keywords])
    console.print(Panel.fit(
        f"[cyan]Analyzing:[/cyan] {report.url}\n"
        f"[cyan]Focus Keywords:[/cyan] {keywords_str}",
        border_style="blue"
    ))
    console.print()
    
    console.print("━" * 60, style="blue")
    console.print("[bold blue]📊 SEO ANALYSIS REPORT[/bold blue]", justify="center")
    console.print("━" * 60, style="blue")
    console.print()
    
    score_color = get_score_color(report.overall_score)
    console.print(f"[bold {score_color}]🎯 OVERALL SEO SCORE: {report.overall_score}/100[/bold {score_color}]")
    console.print()
    
    console.print(Panel(
        f"[bold]Keyword Cluster Performance: {report.keyword_cluster.cluster_score}/100[/bold]",
        border_style=get_score_color(report.keyword_cluster.cluster_score)
    ))
    console.print()
    
    console.print("[bold]📈 Individual Keyword Scores:[/bold]")
    console.print()
    
    for kw_score in report.keyword_cluster.individual_scores:
        score_color = get_score_color(kw_score.score)
        icon = get_score_icon(kw_score.score)
        
        console.print(f"{icon} [bold]\"{kw_score.keyword}\"[/bold] - [{score_color}]{kw_score.score}/100[/{score_color}]")
        console.print(f"   ├─ Title: {format_bool(kw_score.in_title)}")
        console.print(f"   ├─ Meta: {format_bool(kw_score.in_meta)}")
        console.print(f"   ├─ H1: {format_bool(kw_score.in_h1)}")
        console.print(f"   ├─ Density: {kw_score.density:.1f}%")
        console.print(f"   └─ First 100 words: {format_bool(kw_score.in_first_100_words)}")
        
        if kw_score.recommendations:
            for rec in kw_score.recommendations[:2]:
                console.print(f"      💡 {rec}", style="yellow")
        
        console.print()
    
    console.print("━" * 60, style="blue")
    console.print()
    
    console.print(f"{get_score_icon(report.technical_seo.score)} [bold]Technical SEO: {report.technical_seo.score}/100[/bold]")
    if verbose and report.technical_seo.details:
        for key, value in report.technical_seo.details.items():
            if isinstance(value, dict) and 'present' in value:
                console.print(f"   ├─ {key.title()}: {format_bool(value['present'])}")
    console.print()
    
    console.print(f"{get_score_icon(report.content_analysis.score)} [bold]Content Analysis: {report.content_analysis.score}/100[/bold]")
    if verbose:
        console.print(f"   ├─ Word Count: {report.content_analysis.details['word_count']}")
        console.print(f"   └─ Adequate Length: {format_bool(report.content_analysis.details['adequate_length'])}")
    console.print()
    
    console.print(f"{get_score_icon(report.structure_analysis.score)} [bold]Structure: {report.structure_analysis.score}/100[/bold]")
    if verbose and 'h1' in report.structure_analysis.details:
        h1_info = report.structure_analysis.details['h1']
        console.print(f"   └─ H1 Count: {h1_info['count']}")
    console.print()
    
    console.print(f"{get_score_icon(report.link_analysis.score)} [bold]Links: {report.link_analysis.score}/100[/bold]")
    if verbose:
        internal = report.link_analysis.details['internal_links']['count']
        external = report.link_analysis.details['external_links']['count']
        console.print(f"   ├─ Internal Links: {internal}")
        console.print(f"   └─ External Links: {external}")
    console.print()
    
    if report.ai_analysis:
        if report.ai_analysis.status == 'failed':
            console.print("━" * 60, style="blue")
            console.print("[bold yellow]🤖 AI-POWERED SEO INSIGHTS[/bold yellow]")
            console.print("━" * 60, style="blue")
            console.print()
            error_msg = report.ai_analysis.details.get('error', 'Unknown error')
            console.print(f"[yellow]⚠️  AI features unavailable: {error_msg}[/yellow]")
            if 'ANTHROPIC_API_KEY not configured' in error_msg:
                console.print("[dim]Add ANTHROPIC_API_KEY environment variable to enable AI features[/dim]")
            console.print()
        elif report.ai_analysis.status == 'passed':
            console.print("━" * 60, style="blue")
            console.print("[bold magenta]🤖 AI-POWERED SEO INSIGHTS[/bold magenta]")
            console.print("━" * 60, style="blue")
            console.print()
            
            ai_details = report.ai_analysis.details
            
            if 'optimized_title' in ai_details and ai_details['optimized_title']:
                console.print("[bold]📝 AI-Optimized Title:[/bold]")
                console.print(f"   {ai_details['optimized_title']}")
                console.print()
            
            if 'optimized_meta_description' in ai_details and ai_details['optimized_meta_description']:
                console.print("[bold]📄 AI-Optimized Meta Description:[/bold]")
                console.print(f"   {ai_details['optimized_meta_description']}")
                console.print()
            
            if 'content_quality_analysis' in ai_details and ai_details['content_quality_analysis']:
                quality = ai_details['content_quality_analysis']
                console.print("[bold]📊 Content Quality Analysis:[/bold]")
                if 'readability' in quality:
                    console.print(f"   ├─ Readability: {quality['readability']}/10")
                if 'engagement' in quality:
                    console.print(f"   ├─ Engagement: {quality['engagement']}/10")
                if 'content_value' in quality:
                    console.print(f"   └─ Content Value: {quality['content_value']}/10")
                console.print()
            
            if 'grammar_analysis' in ai_details and ai_details['grammar_analysis']:
                grammar = ai_details['grammar_analysis']
                if 'error' not in grammar:
                    console.print("[bold green]✍️  Grammar & Readability (SEO-Safe):[/bold green]")
                    if 'grammar_score' in grammar:
                        score_color = get_score_color(grammar['grammar_score'] * 10)
                        console.print(f"   ├─ Grammar Score: [{score_color}]{grammar['grammar_score']}/10[/{score_color}]")
                    if 'issues_found' in grammar:
                        console.print(f"   ├─ Issues Found: {grammar['issues_found']}")
                    if 'seo_preserved' in grammar:
                        console.print(f"   └─ SEO Keywords Preserved: {format_bool(grammar['seo_preserved'])}")
                    console.print()
                    
                    if 'title_improvement' in grammar and grammar['title_improvement']:
                        console.print("[dim]   Improved Title (Keywords Preserved):[/dim]")
                        console.print(f"   [green]{grammar['title_improvement']}[/green]")
                        console.print()
                    
                    if 'meta_improvement' in grammar and grammar['meta_improvement']:
                        console.print("[dim]   Improved Meta Description (Keywords Preserved):[/dim]")
                        console.print(f"   [green]{grammar['meta_improvement']}[/green]")
                        console.print()
                    
                    if 'grammar_suggestions' in grammar and grammar['grammar_suggestions']:
                        console.print("[bold]   Grammar Fixes:[/bold]")
                        for i, suggestion in enumerate(grammar['grammar_suggestions'][:3], 1):
                            console.print(f"   • {suggestion}")
                        console.print()
                    
                    if 'readability_tips' in grammar and grammar['readability_tips']:
                        console.print("[bold]   Readability Tips:[/bold]")
                        for tip in grammar['readability_tips'][:2]:
                            console.print(f"   • {tip}")
                        console.print()
            
            if 'ai_recommendations' in ai_details and ai_details['ai_recommendations']:
                console.print("[bold magenta]💡 AI Recommendations:[/bold magenta]")
                for i, rec in enumerate(ai_details['ai_recommendations'], 1):
                    console.print(f"   {i}. {rec}")
                console.print()
    
    if report.top_recommendations:
        console.print("━" * 60, style="blue")
        console.print("[bold blue]🎯 TOP RECOMMENDATIONS[/bold blue]")
        console.print("━" * 60, style="blue")
        console.print()
        
        for i, rec in enumerate(report.top_recommendations, 1):
            console.print(f"{i}. 🔴 {rec}")
        
        console.print()
    
    console.print("━" * 60, style="blue")
    console.print()

def get_score_color(score: int) -> str:
    if score >= 80:
        return "green"
    elif score >= 60:
        return "yellow"
    else:
        return "red"

def get_score_icon(score: int) -> str:
    if score >= 80:
        return "✅"
    elif score >= 60:
        return "⚠️"
    else:
        return "❌"

def format_bool(value: bool) -> str:
    return "[green]✓ Yes[/green]" if value else "[red]✗ No[/red]"

def show_progress(message: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        progress.add_task(description=message, total=None)
