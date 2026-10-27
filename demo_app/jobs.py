import threading

import requests


def fetch_status(url: str) -> int:
    """Fetch a URL in a background job and return the HTTP status code."""
    response = requests.get(url, timeout=10)
    return response.status_code


def start_sync_job(url: str) -> threading.Thread:
    """Start fetch_status in a daemon thread."""
    thread = threading.Thread(target=fetch_status, args=(url,), daemon=True)
    thread.start()
    return thread
