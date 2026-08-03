from src.core.scoring import (
    calculate_overall_score,
    calculate_keyword_score,
    get_status,
)


class TestCalculateOverallScore:
    def test_perfect_scores(self):
        score = calculate_overall_score(100, 100, 100, 100, 100)
        assert score == 100

    def test_zero_scores(self):
        score = calculate_overall_score(0, 0, 0, 0, 0)
        assert score == 0

    def test_weighted_mix(self):
        # keyword 40%, technical 20%, content 20%, structure 10%, links 10%
        score = calculate_overall_score(100, 0, 0, 0, 0)
        assert score == 40

    def test_clamped_to_100(self):
        score = calculate_overall_score(100, 100, 100, 100, 100)
        assert 0 <= score <= 100


class TestCalculateKeywordScore:
    def test_all_signals(self):
        score = calculate_keyword_score(
            in_title=True,
            in_meta=True,
            in_h1=True,
            in_headings=2,
            in_first_100_words=True,
            density_score=100.0,
            distribution_score=100.0,
        )
        assert score == 100

    def test_no_signals(self):
        score = calculate_keyword_score(
            in_title=False,
            in_meta=False,
            in_h1=False,
            in_headings=0,
            in_first_100_words=False,
            density_score=0.0,
            distribution_score=0.0,
        )
        assert score == 0


class TestGetStatus:
    def test_passed(self):
        assert get_status(80) == "passed"
        assert get_status(95) == "passed"

    def test_warning(self):
        assert get_status(60) == "warning"
        assert get_status(79) == "warning"

    def test_failed(self):
        assert get_status(0) == "failed"
        assert get_status(59) == "failed"
