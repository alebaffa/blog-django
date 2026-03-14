"""
Mastodon public API service.

- No authentication required for public accounts.
- Account ID is resolved once and cached indefinitely (it never changes).
- Statuses are cached for 15 minutes to avoid hammering the instance.
"""

import requests
from django.core.cache import cache

INSTANCE = "https://famichiki.jp"
ACCOUNT = "alebaffa2"
CACHE_KEY_ACCOUNT_ID = "mastodon_account_id"
CACHE_KEY_STATUSES = "mastodon_statuses"
CACHE_TTL = 60 * 15  # 15 minutes


def _resolve_account_id():
    account_id = cache.get(CACHE_KEY_ACCOUNT_ID)
    if account_id:
        return account_id

    url = f"{INSTANCE}/api/v1/accounts/lookup"
    response = requests.get(url, params={"acct": ACCOUNT}, timeout=10)
    response.raise_for_status()
    account_id = response.json()["id"]
    cache.set(CACHE_KEY_ACCOUNT_ID, account_id)  # cache forever — ID never changes
    return account_id


def get_statuses():
    """
    Return (posts, replies) as two lists of Mastodon status objects.
    Posts are original toots; replies are responses to others.
    Results are cached for 15 minutes.
    """
    cached = cache.get(CACHE_KEY_STATUSES)
    if cached is not None:
        return cached

    account_id = _resolve_account_id()
    url = f"{INSTANCE}/api/v1/accounts/{account_id}/statuses"
    response = requests.get(
        url,
        params={"limit": 40, "exclude_reblogs": "true"},
        timeout=10,
    )
    response.raise_for_status()

    statuses = response.json()
    posts = [s for s in statuses if s.get("in_reply_to_id") is None][:5]
    replies = [s for s in statuses if s.get("in_reply_to_id") is not None][:5]

    result = (posts, replies)
    cache.set(CACHE_KEY_STATUSES, result, CACHE_TTL)
    return result
