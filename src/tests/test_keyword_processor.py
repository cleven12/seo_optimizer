from src.core.keyword_processor import (
    process_keyword,
    process_keywords,
    match_keyword_in_text,
)


class TestProcessKeyword:
    def test_basic_keyword(self):
        result = process_keyword("SEO Optimization")
        assert result.original == "SEO Optimization"
        assert result.stemmed
        assert isinstance(result.variations, list)
        assert len(result.variations) >= 1

    def test_strips_whitespace(self):
        result = process_keyword("  ranking  ")
        assert result.original == "ranking"


class TestProcessKeywords:
    def test_list(self):
        results = process_keywords(["seo", "content marketing"])
        assert len(results) == 2


class TestMatchKeywordInText:
    def test_exact_match(self):
        kw = process_keyword("python tutorial")
        assert match_keyword_in_text(kw, "This is a Python tutorial for beginners") is True

    def test_no_match(self):
        kw = process_keyword("quantum physics")
        assert match_keyword_in_text(kw, "Learn web development with Django") is False

    def test_empty_text(self):
        kw = process_keyword("seo")
        assert match_keyword_in_text(kw, "") is False
