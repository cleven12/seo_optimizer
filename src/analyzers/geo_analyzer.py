"""Generative Engine Optimization (GEO) Analyzer.

Grounded in foundational research:
- Aggarwal et al. (2023/2024), "GEO: Generative Engine Optimization",
  Princeton University, Georgia Tech, Allen Institute for AI, IIT Delhi.
- Empirical studies on generative citation factors (Perplexity, SearchGPT, SGE):
  Authoritative quotations, statistical density, RAG passage salience,
  Schema.org machine readability, and content fluency.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup

from src.analyzers.base_analyzer import BaseAnalyzer
from src.core.scoring import ModuleResult, get_status


# Scientific weights based on Aggarwal et al. impression gain findings
GEO_WEIGHTS = {
    "citation_and_quotations": 0.25,
    "statistical_density": 0.25,
    "passage_salience": 0.20,
    "structured_data": 0.15,
    "readability_fluency": 0.15,
}

# Optimal ranges
OPTIMAL_STAT_DENSITY_MIN = 1.0  # stats per 100 words
OPTIMAL_STAT_DENSITY_MAX = 8.0
OPTIMAL_RAG_CHUNK_MIN = 20     # words per direct answer paragraph (industry standard 20-80 words)
OPTIMAL_RAG_CHUNK_MAX = 90
OPTIMAL_FLESCH_MIN = 30.0      # technical/substantive content threshold
OPTIMAL_FLESCH_MAX = 75.0

# Attribution regex patterns
ATTRIBUTION_PATTERNS = [
    r"(?i:\baccording\s+to\s+)(?:(?:Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s+)?[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,4}",
    r"(?i:\b(?:study|research|survey|report)\s+(?:by|from|conducted\s+by)\s+)(?:(?:Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s+)?[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,4}",
    r"(?i:\b(?:as\s+stated|as\s+noted|as\s+reported)\s+by\s+)(?:(?:Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s+)?[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,4}",
    r"(?i:\bpublished\s+in\s+)[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,4}",
    r"(?i:\b(?:researchers|scientists|analysts|experts)\s+at\s+)[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*){0,4}",
    r"\b[A-Z][a-z]+\s+et\s+al\.",
    r"\([A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?,\s*(?:19|20)\d{2}\)",
]

# Interrogative heading patterns (questions that trigger answer generation)
QUESTION_HEADING_PATTERN = re.compile(
    r"(?:^|[:\d\.\-\s])\b(?:what|how|why|when|where|which|who|can|is|are|do|does|will|should)\b|\?$",
    re.IGNORECASE,
)


@dataclass
class GEOScoreDetails:
    total_score: int
    citation_score: int
    statistical_score: int
    salience_score: int
    schema_score: int
    readability_score: int
    metrics: Dict[str, Any]


class GEOAnalyzer(BaseAnalyzer):
    """Analyzes web content for Generative Engine Optimization (GEO)."""

    def analyze(self) -> ModuleResult:
        recommendations: List[str] = []

        citation_score, citation_metrics, citation_recs = self._analyze_citations_and_quotes()
        stat_score, stat_metrics, stat_recs = self._analyze_statistical_density()
        salience_score, salience_metrics, salience_recs = self._analyze_passage_salience()
        schema_score, schema_metrics, schema_recs = self._analyze_structured_data()
        readability_score, readability_metrics, readability_recs = self._analyze_readability()

        recommendations.extend(citation_recs)
        recommendations.extend(stat_recs)
        recommendations.extend(salience_recs)
        recommendations.extend(schema_recs)
        recommendations.extend(readability_recs)

        weighted_score = (
            citation_score * GEO_WEIGHTS["citation_and_quotations"]
            + stat_score * GEO_WEIGHTS["statistical_density"]
            + salience_score * GEO_WEIGHTS["passage_salience"]
            + schema_score * GEO_WEIGHTS["structured_data"]
            + readability_score * GEO_WEIGHTS["readability_fluency"]
        )
        total_score = min(100, max(0, int(round(weighted_score))))

        details = {
            "geo_score": total_score,
            "sub_scores": {
                "citations_and_quotations": citation_score,
                "statistical_density": stat_score,
                "passage_salience": salience_score,
                "structured_data": schema_score,
                "readability_fluency": readability_score,
            },
            "metrics": {
                "citations": citation_metrics,
                "statistics": stat_metrics,
                "salience": salience_metrics,
                "structured_data": schema_metrics,
                "readability": readability_metrics,
            },
        }

        return ModuleResult(
            module_name="Generative Engine Optimization (GEO)",
            score=total_score,
            status=get_status(total_score),
            details=details,
            recommendations=recommendations,
        )

    def _analyze_citations_and_quotes(self) -> Tuple[int, Dict[str, Any], List[str]]:
        """Evaluate direct quotations, citation tags, and authoritative attributions."""
        recs: List[str] = []
        soup = self._get_raw_soup()

        # HTML-level quote and citation tags
        blockquotes = soup.find_all(["blockquote", "q"])
        cite_tags = soup.find_all("cite")

        text = self.content.body_text or ""

        # Inline quotes: "...", “...”, ‘...’, «...»
        inline_quotes = re.findall(r'["“«‘][^"”»’]{10,250}["”»’]', text)

        # Authoritative attribution detection
        attribution_matches = []
        for pattern in ATTRIBUTION_PATTERNS:
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            attribution_matches.extend(matches)

        quote_count = len(blockquotes) + len(inline_quotes)
        citation_count = len(cite_tags) + len(attribution_matches)

        # Scoring
        score = 0
        if quote_count >= 3 and citation_count >= 2:
            score = 100
        elif quote_count >= 2 and citation_count >= 1:
            score = 85
        elif quote_count >= 1 or citation_count >= 1:
            score = 60
        elif quote_count > 0:
            score = 45
        else:
            score = 20

        if quote_count == 0:
            recs.append(
                "Add direct authoritative quotations (e.g. industry experts, official studies) to improve generative citation probability by up to 30-40% (Aggarwal et al., 2023)."
            )
        elif citation_count == 0:
            recs.append(
                "Attribute your claims to named sources (e.g. 'According to [Source]', '(Author, Year)') so LLMs can verify and cite your content."
            )

        metrics = {
            "blockquote_count": len(blockquotes),
            "inline_quote_count": len(inline_quotes),
            "cite_tag_count": len(cite_tags),
            "attribution_count": len(attribution_matches),
            "total_quotes": quote_count,
            "total_citations": citation_count,
        }
        return score, metrics, recs

    def _analyze_statistical_density(self) -> Tuple[int, Dict[str, Any], List[str]]:
        """Calculate statistical and quantitative evidence density per 100 words."""
        recs: List[str] = []
        text = self.content.body_text or ""
        word_count = max(1, self.content.word_count)

        # Percentages: 45%, 12.5 percent
        percentages = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|percent\b|percentage\b)", text, re.IGNORECASE)

        # Currency figures: $500, €1.2M, £45,000, 500 USD
        currencies = re.findall(r"(?:[\$€£¥]\s*\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:billion|million|k|m|b))?|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:USD|EUR|GBP|dollars|euros)\b)", text, re.IGNORECASE)

        # Quantitative metrics: 250 ms, 10x, 3.5 years, 10,000 users, 100 MB/s
        metrics_found = re.findall(r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:x|times|fold|years|months|days|hours|minutes|seconds|users|customers|queries|tokens|GB|MB|TB|PB|KB|ms|kg|km|GHz|MHz|fps|mph|km/h|Gbps|Mbps|MB/s|KB/s)\b", text, re.IGNORECASE)

        # Statistical ratios / formulas: 1 in 4, p < 0.05, n = 500, r = 0.85
        stats_terms = re.findall(r"\b(?:p\s*[<>=]\s*0?\.\d+|r\s*[<>=]\s*-?0?\.\d+|R\^?2\s*[<>=]\s*0?\.\d+|n\s*=\s*\d+|\d+\s+in\s+\d+|\d+\s+out\s+of\s+\d+|\d+\s*:\s*\d+)\b", text, re.IGNORECASE)

        total_stats = len(percentages) + len(currencies) + len(metrics_found) + len(stats_terms)
        stat_density = (total_stats / (word_count / 100.0))

        if OPTIMAL_STAT_DENSITY_MIN <= stat_density <= OPTIMAL_STAT_DENSITY_MAX:
            score = 100
        elif 0.5 <= stat_density < OPTIMAL_STAT_DENSITY_MIN:
            score = int(50 + (stat_density / OPTIMAL_STAT_DENSITY_MIN) * 45)
            recs.append(
                f"Increase quantitative data density (currently {stat_density:.1f} stats/100 words, optimal is {OPTIMAL_STAT_DENSITY_MIN}-{OPTIMAL_STAT_DENSITY_MAX}). Empirical data increases generative engine citations by ~37%."
            )
        elif stat_density > OPTIMAL_STAT_DENSITY_MAX:
            score = max(60, int(100 - (stat_density - OPTIMAL_STAT_DENSITY_MAX) * 8))
            recs.append(
                f"Statistical density is high ({stat_density:.1f} stats/100 words). Ensure numbers are contextualized with explanatory analysis."
            )
        else:
            score = int(max(10, stat_density * 80))
            recs.append(
                "Include specific statistics, percentages, and metrics to provide concrete facts for generative models to cite."
            )

        metrics = {
            "total_stats_found": total_stats,
            "stat_density_per_100_words": round(stat_density, 2),
            "percentages_count": len(percentages),
            "currencies_count": len(currencies),
            "metrics_count": len(metrics_found),
            "statistical_terms_count": len(stats_terms),
        }
        return score, metrics, recs

    def _analyze_passage_salience(self) -> Tuple[int, Dict[str, Any], List[str]]:
        """Evaluate question headings and concise direct declarative answers for RAG."""
        recs: List[str] = []
        soup = self._get_raw_soup()

        question_headings = []
        direct_answers = []

        headings = soup.find_all(["h2", "h3", "h4"])
        for h in headings:
            h_text = h.get_text().strip()
            if QUESTION_HEADING_PATTERN.search(h_text):
                question_headings.append(h_text)
                # Find subsequent paragraph before any next heading
                next_elem = h.find_next(["p", "h1", "h2", "h3", "h4", "h5", "h6"])
                if next_elem and next_elem.name == "p":
                    p_words = next_elem.get_text().split()
                    word_len = len(p_words)
                    if OPTIMAL_RAG_CHUNK_MIN <= word_len <= OPTIMAL_RAG_CHUNK_MAX:
                        direct_answers.append({
                            "heading": h_text,
                            "word_count": word_len,
                            "snippet": " ".join(p_words[:12]) + "...",
                        })

        total_q = len(question_headings)
        answered_q = len(direct_answers)

        score = 0
        if total_q >= 2 and answered_q >= 2:
            score = 100
        elif total_q >= 1 and answered_q >= 1:
            score = 80
        elif total_q >= 1 and answered_q == 0:
            score = 55
            recs.append(
                f"Question headings found ({total_q}), but following paragraphs lack concise direct answers ({OPTIMAL_RAG_CHUNK_MIN}-{OPTIMAL_RAG_CHUNK_MAX} words). Generative search engines prioritize concise, direct answer passages immediately under question headers."
            )
        else:
            score = 30
            recs.append(
                "Format key sections with question headings (e.g. 'What is...', 'How does...') followed immediately by a 40-70 word direct answer to maximize RAG passage retrieval."
            )

        metrics = {
            "question_headings_count": total_q,
            "direct_answers_count": answered_q,
            "question_headings": question_headings[:5],
            "direct_answers": direct_answers[:5],
        }
        return score, metrics, recs

    def _analyze_structured_data(self) -> Tuple[int, Dict[str, Any], List[str]]:
        """Validate Schema.org JSON-LD structured data for generative search crawlers."""
        recs: List[str] = []
        soup = self._get_raw_soup()

        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        schemas: List[Dict[str, Any]] = []
        detected_types: List[str] = []

        for s in scripts:
            try:
                raw = s.string or s.get_text()
                if not raw:
                    continue
                data = json.loads(raw.strip())
                if isinstance(data, dict):
                    if "@graph" in data and isinstance(data["@graph"], list):
                        for item in data["@graph"]:
                            if isinstance(item, dict):
                                schemas.append(item)
                                if isinstance(item.get("@type"), list):
                                    detected_types.extend(str(t) for t in item["@type"])
                                elif "@type" in item:
                                    detected_types.append(str(item["@type"]))
                    else:
                        schemas.append(data)
                        if isinstance(data.get("@type"), list):
                            detected_types.extend(str(t) for t in data["@type"])
                        elif "@type" in data:
                            detected_types.append(str(data["@type"]))
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            schemas.append(item)
                            if isinstance(item.get("@type"), list):
                                detected_types.extend(str(t) for t in item["@type"])
                            elif "@type" in item:
                                detected_types.append(str(item["@type"]))
            except Exception:
                pass

        has_schema = len(schemas) > 0
        has_essential_fields = False

        if has_schema:
            for s in schemas:
                # Check for essential properties that generative models rely on
                has_name = bool(s.get("name") or s.get("headline"))
                has_desc = bool(s.get("description") or s.get("mainEntity") or s.get("itemListElement") or s.get("articleBody"))
                if has_name and has_desc:
                    has_essential_fields = True
                    break

        score = 0
        if has_schema and has_essential_fields:
            score = 100
        elif has_schema:
            score = 70
            recs.append(
                "Schema.org JSON-LD is present but missing essential fields ('name'/'headline' and 'description'). Complete these for richer generative engine entity extraction."
            )
        else:
            score = 0
            recs.append(
                "Add Schema.org JSON-LD structured data (Article, FAQPage, or TechArticle). AI crawlers (PerplexityBot, GPTBot, ClaudeBot) prioritize structured entity data for factual answers."
            )

        metrics = {
            "has_json_ld": has_schema,
            "schema_count": len(schemas),
            "detected_types": detected_types,
            "has_essential_fields": has_essential_fields,
        }
        return score, metrics, recs

    def _analyze_readability(self) -> Tuple[int, Dict[str, Any], List[str]]:
        """Calculate Flesch Reading Ease score to assess content fluency."""
        recs: List[str] = []
        text = self.content.body_text or ""
        words = text.split()
        word_count = len(words)

        if word_count < 10:
            return 30, {"flesch_reading_ease": 0.0, "word_count": word_count}, [
                "Content is too brief for fluency analysis. Expand content to improve ranking depth."
            ]

        # Robust sentence extraction: protect decimals and common abbreviations
        cleaned = re.sub(r"(\d+)\.(\d+)", r"\1__DEC__\2", text)
        for abbr in ["Dr.", "Mr.", "Ms.", "Mrs.", "Prof.", "vs.", "e.g.", "i.e.", "U.S.", "Jan.", "Feb.", "Mar.", "Apr.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]:
            cleaned = cleaned.replace(abbr, abbr.replace(".", "__DOT__"))
        sentences = [s.strip().replace("__DEC__", ".").replace("__DOT__", ".") for s in re.split(r"[.!?]+(?:\s+|$)", cleaned) if s.strip()]
        sentence_count = max(1, len(sentences))

        # Syllable count estimation
        total_syllables = sum(self._count_syllables(w) for w in words)

        # Flesch Reading Ease formula
        flesch = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (total_syllables / word_count)
        flesch = round(max(0.0, min(100.0, flesch)), 1)

        if OPTIMAL_FLESCH_MIN <= flesch <= OPTIMAL_FLESCH_MAX:
            score = 100
        elif 20.0 <= flesch < OPTIMAL_FLESCH_MIN:
            score = 75
            recs.append(
                f"Content fluency is complex (Flesch score {flesch}, optimal is {OPTIMAL_FLESCH_MIN}-{OPTIMAL_FLESCH_MAX}). Shorten complex sentences to improve LLM embedding clarity."
            )
        elif flesch > OPTIMAL_FLESCH_MAX:
            score = 85
        else:
            score = max(20, int(flesch * 2.5))
            recs.append(
                f"Content readability is low (Flesch score {flesch}). Simplify convoluted phrasing and split long sentences so AI models can parse key arguments clearly."
            )

        metrics = {
            "flesch_reading_ease": flesch,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "syllables_per_word": round(total_syllables / word_count, 2),
        }
        return score, metrics, recs

    @staticmethod
    def _count_syllables(word: str) -> int:
        """Estimate syllable count of an English word."""
        w = word.lower().strip()
        if not w:
            return 0
        w = re.sub(r"[^a-z]", "", w)
        if len(w) <= 3:
            return 1
        # Remove trailing silent e
        if w.endswith("e") and not w.endswith("le"):
            w = w[:-1]
        vowels = re.findall(r"[aeiouy]+", w)
        return max(1, len(vowels))

    def _get_raw_soup(self) -> BeautifulSoup:
        """Retrieve or reconstruct fresh BeautifulSoup object before script decomposition."""
        if hasattr(self.content, "html") and self.content.html:
            try:
                return BeautifulSoup(self.content.html, "lxml")
            except Exception:
                return BeautifulSoup(self.content.html, "html.parser")
        return self.content.soup
