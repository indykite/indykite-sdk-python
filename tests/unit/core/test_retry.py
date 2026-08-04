"""Retry policy decisions and backoff."""

from __future__ import annotations

from indykite_sdk import RetryConfig
from indykite_sdk._core.retry import retry_delay, should_retry

CONFIG = RetryConfig()


def test_should_retry_retries_idempotent_methods_on_retryable_status() -> None:
    """Should retry retries idempotent methods on retryable status."""
    for method in ("GET", "PUT", "DELETE"):
        for status in (429, 502, 503, 504):
            assert should_retry(CONFIG, method, status, attempt=1)


def test_should_retry_does_not_retry_post_by_default() -> None:
    """Should retry does not retry post by default."""
    assert not should_retry(CONFIG, "POST", 503, attempt=1)


def test_should_retry_retries_post_when_opted_in() -> None:
    """Should retry retries post when opted in."""
    config = RetryConfig(retry_posts=True)
    assert should_retry(config, "POST", 503, attempt=1)


def test_should_retry_does_not_retry_non_retryable_status() -> None:
    """Should retry does not retry non retryable status."""
    for status in (400, 401, 403, 404, 412, 500):
        assert not should_retry(CONFIG, "GET", status, attempt=1)


def test_should_retry_stops_at_max_attempts() -> None:
    """Should retry stops at max attempts."""
    assert should_retry(CONFIG, "GET", 503, attempt=2)
    assert not should_retry(CONFIG, "GET", 503, attempt=3)


def test_should_retry_disabled_config_never_retries() -> None:
    """Should retry disabled config never retries."""
    assert not should_retry(None, "GET", 503, attempt=1)


def test_retry_delay_exponential_backoff_within_bounds() -> None:
    """Retry delay exponential backoff within bounds."""
    for attempt, ceiling in ((1, 0.5), (2, 1.0), (3, 2.0), (4, 4.0), (10, 4.0)):
        delay = retry_delay(CONFIG, attempt)
        assert 0 <= delay <= ceiling


def test_retry_delay_retry_after_header_wins() -> None:
    """Retry delay retry after header wins."""
    assert retry_delay(CONFIG, 1, retry_after="7") == 7.0


def test_retry_delay_malformed_retry_after_falls_back_to_backoff() -> None:
    """Retry delay malformed retry after falls back to backoff."""
    assert retry_delay(CONFIG, 1, retry_after="soon") <= 0.5
