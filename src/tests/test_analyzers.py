"""Smoke tests for analyzer modules with minimal HTML fixtures."""

from bs4 import BeautifulSoup

from src.analyzers.content_analyzer import ContentAnalyzer
from src.analyzers.link_analyzer import LinkAnalyzer
from src.analyzers.structure_analyzer import StructureAnalyzer
from src.analyzers.technical_seo import TechnicalSEOAnalyzer
from src.core.fetcher import WebContent
from src.core.keyword_processor import process_keywords
from src.core.scoring import ModuleResult


SAMPLE_HTML = """
<html>
  <head>
    <title>Python SEO Guide for Beginners</title>
    <meta name="description" content="A complete Python SEO guide for beginners who want better rankings and content quality online.">
    <link rel="canonical" href="https://example.com/python-seo">
    <meta property="og:title" content="Python SEO Guide">
  </head>
  <body>
    <h1>Python SEO Guide</h1>
    <h2>Getting started</h2>
    <p>Python SEO guide content helps beginners learn optimization. """ + ("More words about Python SEO. " * 40) + """</p>
    <a href="/blog">Internal post</a>
    <a href="https://docs.python.org">External docs</a>
    <img src="chart.png" alt="SEO chart">
  </body>
</html>
"""


def _sample_content():
    soup = BeautifulSoup(SAMPLE_HTML, "lxml")
    return WebContent("https://example.com/python-seo", SAMPLE_HTML, soup)


def _keywords():
    return process_keywords(["python seo", "beginners"])


def test_technical_seo_returns_module_result():
    result = TechnicalSEOAnalyzer(_sample_content(), _keywords()).analyze()
    assert isinstance(result, ModuleResult)
    assert 0 <= result.score <= 100


def test_content_analyzer_returns_module_result():
    result = ContentAnalyzer(_sample_content(), _keywords()).analyze()
    assert isinstance(result, ModuleResult)
    assert 0 <= result.score <= 100


def test_structure_analyzer_returns_module_result():
    result = StructureAnalyzer(_sample_content(), _keywords()).analyze()
    assert isinstance(result, ModuleResult)
    assert 0 <= result.score <= 100


def test_link_analyzer_returns_module_result():
    result = LinkAnalyzer(_sample_content(), _keywords()).analyze()
    assert isinstance(result, ModuleResult)
    assert 0 <= result.score <= 100
