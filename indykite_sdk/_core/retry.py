"""Retry policy for API requests.

Only idempotent methods (GET, PUT, DELETE) are retried by default; POST is
never retried unless ``retry_posts=True`` is set, because Capture/ContX IQ
writes are not guaranteed idempotent. Connect-level retries are handled
separately by the httpx transport.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

RETRYABLE_STATUSES = frozenset({429, 502, 503, 504})
_IDEMPOTENT_METHODS = frozenset({"GET", "PUT", "DELETE"})


@dataclass(frozen=True, slots=True)
class RetryConfig:
    """Retry behavior for failed requests.

    Attributes:
        max_attempts: Total attempts per request, including the first one.
        backoff_initial: Delay before the first retry, in seconds.
        backoff_max: Upper bound for the exponential backoff delay.
        retry_statuses: HTTP statuses that trigger a retry.
        retry_posts: Also retry POST requests. Enable only when your POSTs are
            idempotent (e.g. capture upserts keyed by ``external_id``).
    """

    max_attempts: int = 3
    backoff_initial: float = 0.5
    backoff_max: float = 4.0
    retry_statuses: frozenset[int] = RETRYABLE_STATUSES
    retry_posts: bool = False


DEFAULT_RETRY = RetryConfig()


def should_retry(config: RetryConfig | None, method: str, status_code: int, attempt: int) -> bool:
    """Whether ``attempt`` (1-based) for ``method`` ending in ``status_code`` should be retried."""
    if config is None or attempt >= config.max_attempts:
        return False
    if status_code not in config.retry_statuses:
        return False
    return method.upper() in _IDEMPOTENT_METHODS or (method.upper() == "POST" and config.retry_posts)


def retry_delay(config: RetryConfig, attempt: int, retry_after: str | None = None) -> float:
    """Delay in seconds before retry number ``attempt`` (1-based), honoring ``Retry-After``."""
    if retry_after:
        try:
            return max(0.0, float(retry_after))
        except ValueError:
            pass
    delay = min(config.backoff_initial * (2 ** (attempt - 1)), config.backoff_max)
    return delay * random.uniform(0.5, 1.0)  # noqa: S311 # nosec B311 - jitter, not cryptography
