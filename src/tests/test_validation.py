import pytest

from src.utils.validation import is_valid_url, validate_keywords


class TestIsValidUrl:
    def test_https_url(self):
        assert is_valid_url("https://example.com") is True

    def test_http_url(self):
        assert is_valid_url("http://example.com/path") is True

    def test_with_query(self):
        assert is_valid_url("https://example.com/page?q=seo") is True

    def test_missing_scheme(self):
        assert is_valid_url("example.com") is False

    def test_empty(self):
        assert is_valid_url("") is False

    def test_garbage(self):
        assert is_valid_url("not a url") is False


class TestValidateKeywords:
    def test_single_keyword(self):
        assert validate_keywords("seo") == ["seo"]

    def test_multiple_keywords(self):
        assert validate_keywords("seo, content marketing, ranking") == [
            "seo",
            "content marketing",
            "ranking",
        ]

    def test_trims_whitespace(self):
        assert validate_keywords("  python ,  django  ") == ["python", "django"]

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty"):
            validate_keywords("")

    def test_only_commas_raises(self):
        with pytest.raises(ValueError):
            validate_keywords(" , , ")
