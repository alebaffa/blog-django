"""
WaniKani API service.

Best practices followed:
- Pagination: fetches all pages via pages.next_url
- Caching: aggregated stats cached for 1 hour via Django cache
- Conditional requests: ETag stored and sent as If-None-Match on re-fetch
- Rate limit: single aggregation pass; cache prevents hammering the API
"""
import os
import requests
from django.core.cache import cache

API_BASE = 'https://api.wanikani.com/v2'
CACHE_KEY_STATS = 'wanikani_stats'
CACHE_KEY_ETAG = 'wanikani_etag'
CACHE_TTL = 60 * 60  # 1 hour

SUBJECT_TYPES = ('radical', 'kanji', 'vocabulary', 'kana_vocabulary')


def _api_token():
    return os.environ.get('WANIKANI_API_TOKEN', '')


def _fetch_all_review_statistics():
    """Fetch every page of /review_statistics and return the raw list of data objects."""
    token = _api_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Wanikani-Revision': '20170710',
    }

    etag = cache.get(CACHE_KEY_ETAG)
    if etag:
        headers['If-None-Match'] = etag

    url = f'{API_BASE}/review_statistics'
    all_items = []

    while url:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 304:
            # Not modified — return None to signal caller to use cache
            return None

        response.raise_for_status()

        # Store ETag for the first page only (subsequent pages share session state)
        if url == f'{API_BASE}/review_statistics' and 'ETag' in response.headers:
            cache.set(CACHE_KEY_ETAG, response.headers['ETag'], CACHE_TTL)

        payload = response.json()
        all_items.extend(payload.get('data', []))

        url = payload.get('pages', {}).get('next_url')
        # Remove auth from next_url headers since requests carries them via headers dict
    return all_items


def _aggregate(items):
    """Aggregate raw API records into summary stats grouped by subject type."""
    totals = {t: {
        'meaning_correct': 0,
        'meaning_incorrect': 0,
        'reading_correct': 0,
        'reading_incorrect': 0,
        'meaning_max_streak': 0,
        'reading_max_streak': 0,
        'count': 0,
    } for t in SUBJECT_TYPES}

    for item in items:
        d = item.get('data', {})
        t = d.get('subject_type')
        if t not in totals:
            continue
        g = totals[t]
        g['meaning_correct'] += d.get('meaning_correct', 0)
        g['meaning_incorrect'] += d.get('meaning_incorrect', 0)
        g['reading_correct'] += d.get('reading_correct', 0)
        g['reading_incorrect'] += d.get('reading_incorrect', 0)
        g['meaning_max_streak'] = max(g['meaning_max_streak'], d.get('meaning_max_streak', 0))
        g['reading_max_streak'] = max(g['reading_max_streak'], d.get('reading_max_streak', 0))
        g['count'] += 1

    # Derive accuracy percentages
    for t, g in totals.items():
        m_total = g['meaning_correct'] + g['meaning_incorrect']
        r_total = g['reading_correct'] + g['reading_incorrect']
        g['meaning_accuracy'] = round(g['meaning_correct'] / m_total * 100) if m_total else None
        g['reading_accuracy'] = round(g['reading_correct'] / r_total * 100) if r_total else None
        total_correct = g['meaning_correct'] + g['reading_correct']
        total_all = m_total + r_total
        g['overall_accuracy'] = round(total_correct / total_all * 100) if total_all else None

    # Overall across all types
    overall_correct = sum(
        g['meaning_correct'] + g['reading_correct'] for g in totals.values()
    )
    overall_total = sum(
        g['meaning_correct'] + g['meaning_incorrect'] + g['reading_correct'] + g['reading_incorrect']
        for g in totals.values()
    )
    overall_accuracy = round(overall_correct / overall_total * 100) if overall_total else None

    return {
        'by_type': totals,
        'overall_correct': overall_correct,
        'overall_total': overall_total,
        'overall_accuracy': overall_accuracy,
        'total_subjects': sum(g['count'] for g in totals.values()),
    }


def get_stats():
    """
    Return aggregated WaniKani stats, served from cache when possible.
    Returns a dict on success, or raises an exception on API error.
    """
    cached = cache.get(CACHE_KEY_STATS)
    if cached:
        return cached

    items = _fetch_all_review_statistics()

    if items is None:
        # 304 Not Modified — ETag matched, nothing new; extend cache with empty placeholder
        # This shouldn't happen on first load, but guard anyway
        return cache.get(CACHE_KEY_STATS) or {}

    stats = _aggregate(items)
    cache.set(CACHE_KEY_STATS, stats, CACHE_TTL)
    return stats
