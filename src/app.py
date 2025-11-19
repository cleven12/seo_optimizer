import argparse
import sys
from rich.console import Console
from src.utils.validation import is_valid_url, validate_keywords
from src.core.orchestrator import run_analysis
from src.output.cli_renderer import render_report, show_progress
from src.output.json_exporter import export_to_json
from src.utils.text_utils import ensure_nltk_data

console = Console()

def app():
    parser = argparse.ArgumentParser(
        description='SEO Analyzer - Analyze web content for SEO optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-u', '--url',
        required=True,
        help='Target URL to analyze'
    )
    
    parser.add_argument(
        '-k', '--keywords',
        required=True,
        help='Comma-separated focus keywords'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='JSON output file path (optional)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed analysis'
    )
    
    parser.add_argument(
        '--ai',
        action='store_true',
        help='Enable AI-powered SEO recommendations using Claude Anthropic'
    )
    
    args = parser.parse_args()
    
    if not is_valid_url(args.url):
        console.print("[red]Error: Invalid URL format[/red]")
        sys.exit(1)
    
    try:
        keywords = validate_keywords(args.keywords)
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)
    
    try:
        console.print("[cyan]Downloading NLTK data...[/cyan]")
        ensure_nltk_data()
        
        console.print(f"[cyan]Fetching content from {args.url}...[/cyan]")
        report = run_analysis(args.url, keywords, args.verbose, args.ai)
        
        render_report(report, args.verbose)
        
        if args.output:
            export_to_json(report, args.output)
            console.print(f"[green]✅ Report saved to: {args.output}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    app()
