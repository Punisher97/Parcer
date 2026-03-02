from pathlib import Path
import httpx

def save_html(html, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(html, encoding="utf-8")

def fetch_text(url: str, timeout: float = 15.0) -> str:

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) hhru-parser/0.1",
    "Accept-Language": "ru,en;q=0.9",
    }

    try:
        with httpx.Client(headers=headers, timeout=timeout, follow_redirects=True) as client:
            resp = client.get(url)
    except httpx.TimeoutException as e:
        raise RuntimeError(f"Timeout while fetching {url}") from e
    except httpx.HTTPError as e:
        raise RuntimeError(f"HTTP/network error while fetching {url}: {e}") from e
    
    if resp.status_code != 200:

        if resp.status_code == 403:
            raise RuntimeError(f"403 Forbidden for {url} (possible anti-bot block)")
        if resp.status_code == 429:
            raise RuntimeError(f'429 Too Many Requests for {url}')
        raise RuntimeError(f"Bad status {resp.status_code} for {url}")

    return resp.text
