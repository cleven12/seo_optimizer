from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from src.core.fetcher import WebContent, fetch_content


SAMPLE_HTML = """
<html>
  <head>
    <title>Python SEO Guide</title>
    <meta name="description" content="Learn SEO with Python tools.">
  </head>
  <body>
    <h1>Python SEO Guide</h1>
    <p>Optimize content for search engines using Python. Learn ranking tips.</p>
    <a href="/internal">Internal</a>
    <a href="https://external.example">External</a>
    <img src="a.png" alt="diagram">
  </body>
</html>
"""


class TestWebContent:
    def test_extracts_core_fields(self):
        soup = BeautifulSoup(SAMPLE_HTML, "lxml")
        content = WebContent("https://example.com", SAMPLE_HTML, soup)

        assert content.title == "Python SEO Guide"
        assert content.meta_description == "Learn SEO with Python tools."
        assert content.h1 == "Python SEO Guide"
        assert content.word_count > 0
        assert any(img["has_alt"] for img in content.images)
        assert any(link["is_internal"] for link in content.links)
        assert any(link["is_external"] for link in content.links)


class TestFetchContent:
    @patch("src.core.fetcher.requests.get")
    def test_fetch_success(self, mock_get):
        response = MagicMock()
        response.status_code = 200
        response.text = SAMPLE_HTML
        response.content = SAMPLE_HTML.encode("utf-8")
        response.raise_for_status = MagicMock()
        mock_get.return_value = response

        result = fetch_content("https://example.com")
        assert isinstance(result, WebContent)
        assert result.title == "Python SEO Guide"
