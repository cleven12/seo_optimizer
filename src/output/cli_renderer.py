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
    
    console.print("━" * 120, style="blue", justify="full")
    console.print("[bold blue]📊 SEO ANALYSIS REPORT[/bold blue]", justify="center")
    console.print("━" * 120, style="blue", justify="full",)
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
    
    console.print("━" * 120, style="blue")
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
    
    if report.top_recommendations:
        console.print("━" * 120, style="blue")
        console.print("[bold blue]🎯 TOP RECOMMENDATIONS[/bold blue]")
        console.print("━" * 120, style="blue")
        console.print()
        
        for i, rec in enumerate(report.top_recommendations, 1):
            console.print(f"{i}. 🔴 {rec}")
        
        console.print()
    
    console.print("━" * 120, style="blue")
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
