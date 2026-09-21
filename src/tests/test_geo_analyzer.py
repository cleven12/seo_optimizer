"""Tests for Generative Engine Optimization (GEO) Analyzer."""

import json
from bs4 import BeautifulSoup
import pytest

from src.analyzers.geo_analyzer import GEOAnalyzer, GEO_WEIGHTS
from src.core.fetcher import WebContent
from src.core.keyword_processor import process_keywords
from src.core.scoring import ModuleResult


SAMPLE_GEO_RICH_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Generative Engine Optimization (GEO) Strategies for 2026</title>
    <meta name="description" content="Comprehensive guide to Generative Engine Optimization (GEO) and citation strategies for LLM search.">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "TechArticle",
      "headline": "Generative Engine Optimization (GEO) Strategies",
      "description": "Comprehensive guide to Generative Engine Optimization (GEO) and citation strategies for LLM search.",
      "author": {
        "@type": "Person",
        "name": "Alex Mercer"
      },
      "datePublished": "2026-01-15"
    }
    </script>
  </head>
  <body>
    <h1>Generative Engine Optimization (GEO)</h1>

    <h2>What is Generative Engine Optimization?</h2>
    <p>
      Generative Engine Optimization (GEO) optimizes content for AI search engines.
      It helps pages earn citations on platforms like Perplexity, ChatGPT, and Claude.
      Clear writing and verifiable data help AI systems understand your key facts.
      This ensures your work is accurately quoted in generative answers.
    </p>

    <h3>How does statistical density influence AI search?</h3>
    <p>
      According to research by Princeton University and Allen AI, quantitative data increases
      citation rates by up to 37%. Websites with empirical reporting saw a 42% lift in impressions
      across 1,500 queries. Verifiable numbers act as strong anchors for AI retrieval models.
    </p>

    <blockquote>
      "Generative engines prioritize sources that offer direct, factual answers backed by authoritative
      attributions and numerical evidence," published in Academic Research Quarterly.
    </blockquote>

    <p>
      In a study by Stanford analysts, over $2.5M in value was linked to citations.
      More than 10,000 users participated in the trial.
      About 1 in 3 users clicked through to the primary cited source within 45 seconds.
    </p>
  </body>
</html>
"""

SAMPLE_GEO_POOR_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Simple Page</title>
  </head>
  <body>
    <h1>Overview</h1>
    <p>We do things. Things are nice. Everything is great and awesome and good.</p>
  </body>
</html>
"""


def _make_content(html: str, url: str = "https://example.com/geo-guide") -> WebContent:
    soup = BeautifulSoup(html, "lxml")
    return WebContent(url, html, soup)


def _keywords():
    return process_keywords(["generative engine optimization", "geo"])


class TestGEOAnalyzer:
    def test_returns_module_result(self):
        content = _make_content(SAMPLE_GEO_RICH_HTML)
        analyzer = GEOAnalyzer(content, _keywords())
        result = analyzer.analyze()

        assert isinstance(result, ModuleResult)
        assert result.module_name == "Generative Engine Optimization (GEO)"
        assert 0 <= result.score <= 100
        assert result.status in ["passed", "warning", "failed"]
        assert "sub_scores" in result.details
        assert "metrics" in result.details

    def test_rich_content_scores_high(self):
        content = _make_content(SAMPLE_GEO_RICH_HTML)
        result = GEOAnalyzer(content, _keywords()).analyze()

        assert result.score >= 80
        assert result.status == "passed"

        subs = result.details["sub_scores"]
        assert subs["citations_and_quotations"] >= 80
        assert subs["statistical_density"] >= 80
        assert subs["passage_salience"] >= 80
        assert subs["structured_data"] == 100
        assert subs["readability_fluency"] >= 70

    def test_poor_content_scores_low_with_actionable_recommendations(self):
        content = _make_content(SAMPLE_GEO_POOR_HTML)
        result = GEOAnalyzer(content, _keywords()).analyze()

        assert result.score < 60
        assert result.status == "failed"
        assert len(result.recommendations) >= 3

        recs_text = " ".join(result.recommendations)
        assert "quotation" in recs_text.lower() or "source" in recs_text.lower()
        assert "statistic" in recs_text.lower() or "data" in recs_text.lower()
        assert "schema.org" in recs_text.lower() or "json-ld" in recs_text.lower()

    def test_citation_and_quotation_detection(self):
        html = """
        <html>
          <body>
            <p>According to Dr. Jane Doe, the methodology is sound.</p>
            <p>As reported by Nature, the discovery is groundbreaking.</p>
            <blockquote>"Empirical validation is key to reproducible science."</blockquote>
            <cite>Doe et al., 2025</cite>
          </body>
        </html>
        """
        content = _make_content(html)
        score, metrics, recs = GEOAnalyzer(content, _keywords())._analyze_citations_and_quotes()

        assert score >= 85
        assert metrics["total_quotes"] >= 1
        assert metrics["total_citations"] >= 2
        assert metrics["attribution_count"] >= 2

    def test_statistical_density_optimal_and_excessive(self):
        # Optimal content: 2-4 stats in ~80-100 words
        optimal_text = (
            "The experiment showed a 45% increase in throughput. Over 10,000 users reported "
            "improved latency under 50 ms. Revenue grew by $1.2M across several years of testing. "
            "Engineers analyzed performance metrics across diverse benchmark scenarios to ensure reliable results. "
            "The resulting architecture demonstrates strong scalability and resilient throughput under peak conditions."
        )
        html_optimal = f"<html><body><p>{optimal_text}</p></body></html>"
        content_optimal = _make_content(html_optimal)
        score_opt, metrics_opt, _ = GEOAnalyzer(content_optimal, _keywords())._analyze_statistical_density()

        assert score_opt == 100
        assert metrics_opt["stat_density_per_100_words"] >= 1.0

        # Content with zero statistics
        html_zero = "<html><body><p>This is a purely descriptive article without any numbers or figures at all.</p></body></html>"
        content_zero = _make_content(html_zero)
        score_zero, metrics_zero, recs_zero = GEOAnalyzer(content_zero, _keywords())._analyze_statistical_density()

        assert score_zero < 50
        assert metrics_zero["total_stats_found"] == 0
        assert any("statistic" in r.lower() or "metric" in r.lower() for r in recs_zero)

    def test_passage_salience_rag_chunking(self):
        # Question heading followed by 50-word direct answer
        html_salient = """
        <html>
          <body>
            <h2>Why is Schema markup important for AI search?</h2>
            <p>
              Schema markup provides explicit structured metadata that allows search engines and generative models
              to unambiguously parse entity identities, author credentials, and published dates. By eliminating
              semantic ambiguity, websites achieve higher precision during retrieval-augmented generation synthesis,
              ensuring correct attribution and rich interactive snippet rendering.
            </p>
            <h3>How do LLMs select citation passages?</h3>
            <p>
              Large language models evaluate passage salience by measuring semantic similarity between user queries
              and self-contained text passages. Paragraphs that provide immediate declarative answers directly under
              interrogative headers maximize embedding alignment, leading to preferential quotation in generated summaries.
            </p>
          </body>
        </html>
        """
        content = _make_content(html_salient)
        score, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_passage_salience()

        assert score == 100
        assert metrics["question_headings_count"] == 2
        assert metrics["direct_answers_count"] == 2

    def test_structured_data_handling(self):
        # Valid complete schema
        html_valid = """
        <html>
          <head>
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "Article",
              "headline": "Testing GEO",
              "description": "An article about testing GEO algorithms."
            }
            </script>
          </head>
          <body><p>Content</p></body>
        </html>
        """
        content_valid = _make_content(html_valid)
        score_valid, metrics_valid, _ = GEOAnalyzer(content_valid, _keywords())._analyze_structured_data()
        assert score_valid == 100
        assert metrics_valid["has_json_ld"] is True
        assert metrics_valid["has_essential_fields"] is True

        # Incomplete schema (missing description and headline)
        html_incomplete = """
        <html>
          <head>
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "Thing"
            }
            </script>
          </head>
          <body><p>Content</p></body>
        </html>
        """
        content_incomplete = _make_content(html_incomplete)
        score_inc, metrics_inc, recs_inc = GEOAnalyzer(content_incomplete, _keywords())._analyze_structured_data()
        assert score_inc == 70
        assert metrics_inc["has_essential_fields"] is False
        assert any("essential fields" in r.lower() for r in recs_inc)

        # Malformed JSON in script tag
        html_malformed = """
        <html>
          <head>
            <script type="application/ld+json">
            { broken json: true,
            </script>
          </head>
          <body><p>Content</p></body>
        </html>
        """
        content_malformed = _make_content(html_malformed)
        score_mal, metrics_mal, recs_mal = GEOAnalyzer(content_malformed, _keywords())._analyze_structured_data()
        assert score_mal == 0
        assert metrics_mal["has_json_ld"] is False

    def test_readability_fluency_scoring(self):
        # Good readable prose
        readable_text = (
            "Generative Engine Optimization helps your website get found by AI models. "
            "When people search online, AI tools read your articles and create summaries. "
            "If your content is clear and simple, the AI can understand it easily. "
            "This leads to more views and better ranking."
        )
        html = f"<html><body><p>{readable_text}</p></body></html>"
        content = _make_content(html)
        score, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_readability()

        assert score >= 80
        assert metrics["flesch_reading_ease"] >= 50.0

        # Edge case: empty or tiny content
        html_tiny = "<html><body><p>Hello world.</p></body></html>"
        content_tiny = _make_content(html_tiny)
        score_tiny, metrics_tiny, recs_tiny = GEOAnalyzer(content_tiny, _keywords())._analyze_readability()
        assert score_tiny == 30
        assert "brief" in recs_tiny[0].lower()

    def test_weights_integrity(self):
        total_weight = sum(GEO_WEIGHTS.values())
        assert round(total_weight, 5) == 1.0

    def test_percentage_regex_matches_percent_sign(self):
        html = "<html><body><p>Throughput improved by 45% while errors dropped by 12.5% across all nodes.</p></body></html>"
        content = _make_content(html)
        _, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_statistical_density()
        assert metrics["percentages_count"] == 2

    def test_attribution_with_honorific_titles(self):
        html = "<html><body><p>According to Dr. Jane Doe, the methodology is sound. And we can verify it independently.</p></body></html>"
        content = _make_content(html)
        _, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_citations_and_quotes()
        assert metrics["attribution_count"] >= 1

    def test_inline_curly_quotes_detection(self):
        html = "<html><body><p>Experts claim ‘generative optimization will redefine web discoverability in 2026’ without doubt.</p></body></html>"
        content = _make_content(html)
        _, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_citations_and_quotes()
        assert metrics["inline_quote_count"] >= 1

    def test_readability_with_decimals_and_abbreviations(self):
        # A single sentence with decimal numbers and common abbreviations should not split into multiple sentences
        text = "According to Dr. Jane Doe, revenue grew by 4.5% in the U.S. market, which represents a solid milestone."
        html = f"<html><body><p>{text}</p></body></html>"
        content = _make_content(html)
        _, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_readability()
        # Sentence count should be exactly 1, not 5
        assert metrics["sentence_count"] == 1

    def test_passage_salience_with_nested_container(self):
        # Paragraph is nested in a div rather than an immediate sibling
        html = """
        <html>
          <body>
            <h2>What is Generative Engine Optimization?</h2>
            <div class="content-wrapper">
              <p>
                Generative Engine Optimization is the practice of structuring digital content so that AI-powered search
                engines can easily extract, comprehend, and cite the underlying facts and insights in answer summaries.
              </p>
            </div>
            <h3>Why do citations matter in AI answers?</h3>
            <div class="content-wrapper">
              <p>
                Authoritative citations provide verifiable grounding for large language models, reducing hallucinations
                and elevating the credibility score of extracted passages during retrieval-augmented generation.
              </p>
            </div>
          </body>
        </html>
        """
        content = _make_content(html)
        score, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_passage_salience()
        assert score == 100
        assert metrics["direct_answers_count"] == 2

    def test_structured_data_with_list_type_and_alternate_fields(self):
        # Schema with list @type and mainEntity
        html = """
        <html>
          <head>
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": ["TechArticle", "LearningResource"],
              "headline": "Advanced GEO Strategies",
              "mainEntity": {
                "@type": "Question",
                "name": "How does GEO work?"
              }
            }
            </script>
          </head>
          <body><p>Content</p></body>
        </html>
        """
        content = _make_content(html)
        score, metrics, _ = GEOAnalyzer(content, _keywords())._analyze_structured_data()
        assert score == 100
        assert "TechArticle" in metrics["detected_types"]
        assert "LearningResource" in metrics["detected_types"]
        assert metrics["has_essential_fields"] is True

