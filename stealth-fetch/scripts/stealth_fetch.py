#!/usr/bin/env python3
"""
Stealth Fetch — No Mercy Web Scraper
======================================
An automated escalation engine that goes from polite markdown fetcher
to full Cloudflare-busting stealth browser with mobile proxy rotation.

Level 1: Markdown fetcher (fast, free)
Level 2: Scrapling Basic (header/fingerprint randomization)
Level 3: Firecrawl / Browserless.io (cloud rendering)
Level 4: Scrapling Stealth + Mobile Proxy (Cloudflare nuke)

Usage:
    python3 stealth_fetch.py <url> [options]
    python3 stealth_fetch.py "https://bloomberg.com/article" --proxy mobile --human-path
"""

import os
import sys
import json
import time
import random
import argparse
import subprocess
import urllib.parse
import re
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path


# ─── Data Structures ───────────────────────────────────────────────────────────

@dataclass
class FetchResult:
    url: str
    content: str
    level_used: int
    level_name: str
    status_code: Optional[int] = None
    title: Optional[str] = None
    elapsed_ms: int = 0
    proxy_used: Optional[str] = None
    error: Optional[str] = None
    success: bool = True


@dataclass
class FetchConfig:
    proxy_mode: str = "none"          # none | residential | mobile
    start_level: int = 1
    max_level: int = 4
    human_path: bool = False          # Warm cookies via homepage first
    selector: Optional[str] = None   # CSS selector to extract
    timeout_ms: int = 30000
    jitter_min: float = 1.5
    jitter_max: float = 6.0
    verbose: bool = True


# ─── Constants ─────────────────────────────────────────────────────────────────

LEVEL_NAMES = {
    1: "Markdown Fetcher",
    2: "Scrapling Basic",
    3: "Firecrawl/Browserless",
    4: "Scrapling Stealth + Mobile Proxy",
}

# Real browser user agents (rotated per request)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
]

ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9,en-US;q=0.8",
    "en-US,en;q=0.9,es;q=0.8",
    "en-CA,en;q=0.9,fr;q=0.8",
    "en-AU,en;q=0.9",
    "en-US,en;q=0.8,zh-CN;q=0.6",
]

DECODO_PORTS = list(range(10001, 10008))  # 10001-10007


# ─── Proxy Management ──────────────────────────────────────────────────────────

def get_webshare_proxies() -> List[str]:
    """Load Webshare residential proxies from file."""
    proxy_file = os.environ.get("WEBSHARE_PROXY_LIST", "")
    proxies = []
    if not proxy_file:
        return proxies
    try:
        with open(proxy_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split(":")
                    if len(parts) == 4:
                        host, port, user, pw = parts
                        proxies.append(f"http://{user}:{pw}@{host}:{port}")
    except FileNotFoundError:
        pass
    return proxies


def get_decodo_proxy(port: Optional[int] = None) -> str:
    """Get a Decodo mobile proxy URL with optional port rotation."""
    base = os.environ.get("DECODO_MOBILE_PROXY", "")
    if not base:
        return ""
    if port is None:
        port = random.choice(DECODO_PORTS)
    parsed = urllib.parse.urlparse(base)
    new_netloc = f"{parsed.username}:{parsed.password}@{parsed.hostname}:{port}"
    return f"{parsed.scheme}://{new_netloc}"


def pick_proxy(mode: str) -> Optional[str]:
    """Pick a proxy based on mode."""
    if mode == "mobile":
        proxy = get_decodo_proxy()
        return proxy if proxy else None
    elif mode == "residential":
        proxies = get_webshare_proxies()
        return random.choice(proxies) if proxies else None
    return None


def proxy_to_scrapling(proxy_url: str) -> dict:
    """Convert proxy URL to Scrapling dict format."""
    if not proxy_url:
        return {}
    parsed = urllib.parse.urlparse(proxy_url)
    return {
        "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
        "username": parsed.username or "",
        "password": parsed.password or "",
    }


# ─── Header Randomization ──────────────────────────────────────────────────────

def random_headers(ua: Optional[str] = None) -> dict:
    """Generate randomized but realistic browser headers."""
    ua = ua or random.choice(USER_AGENTS)
    is_mobile = "Mobile" in ua or "iPhone" in ua or "Android" in ua
    is_firefox = "Firefox" in ua
    is_safari = "Safari" in ua and "Chrome" not in ua

    headers = {
        "User-Agent": ua,
        "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": random.choice(["1", "0"]),
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    if is_firefox:
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    elif is_safari and not is_mobile:
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    else:
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"

    if not is_firefox and not is_safari:
        headers["sec-ch-ua"] = '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"'
        headers["sec-ch-ua-mobile"] = "?1" if is_mobile else "?0"
        headers["sec-ch-ua-platform"] = '"Android"' if is_mobile else '"Windows"'
        headers["Sec-Fetch-Site"] = random.choice(["none", "same-origin", "cross-site"])
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-User"] = "?1"
        headers["Sec-Fetch-Dest"] = "document"

    return headers


def jitter_sleep(min_s: float = 1.5, max_s: float = 6.0):
    """Sleep for a random human-like duration."""
    delay = random.uniform(min_s, max_s)
    time.sleep(delay)
    return delay


# ─── Detection Helpers ─────────────────────────────────────────────────────────

def is_blocked(content: str, status_code: Optional[int] = None) -> bool:
    """Detect if response is a block page rather than real content."""
    if status_code and status_code in (403, 429, 503, 401, 407):
        return True
    if not content or len(content.strip()) < 200:
        return True
    block_signals = [
        "just a moment",
        "checking your browser",
        "enable javascript and cookies",
        "cf-browser-verification",
        "access denied",
        "403 forbidden",
        "ray id:",
        "cloudflare",
        "perimeterx",
        "datadome",
        "bot detected",
        "please verify you are a human",
        "captcha",
        "i'm under attack mode",
        "ddos protection",
        "attention required",
        "_pxmvid",
        "px-captcha",
    ]
    content_lower = content.lower()
    hits = sum(1 for sig in block_signals if sig in content_lower)
    return hits >= 2


def get_homepage_url(url: str) -> str:
    """Extract homepage URL from any URL."""
    parsed = urllib.parse.urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/"


def find_fetch_markdown_script() -> Optional[str]:
    """Find fetch-markdown.sh in common locations."""
    script_env = os.environ.get("FETCH_MARKDOWN_SCRIPT", "")
    if script_env and Path(script_env).exists():
        return script_env
    # Common locations
    candidates = [
        Path("/root/.openclaw/workspace/scripts/fetch-markdown.sh"),
        Path("/usr/local/bin/fetch-markdown.sh"),
        Path("~/.openclaw/scripts/fetch-markdown.sh").expanduser(),
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


# ─── Level 1: Markdown Fetcher ─────────────────────────────────────────────────

def fetch_level1(url: str, config: FetchConfig) -> FetchResult:
    """Level 1: Use the Cloudflare markdown worker (fastest, if available)."""
    start = time.time()
    script = find_fetch_markdown_script()
    if not script:
        return FetchResult(
            url=url, content="", level_used=1, level_name=LEVEL_NAMES[1],
            elapsed_ms=0, success=False,
            error="fetch-markdown.sh not found. Set FETCH_MARKDOWN_SCRIPT env var or install it."
        )
    try:
        result = subprocess.run(
            [script, url],
            capture_output=True, text=True, timeout=30
        )
        content = result.stdout.strip()
        elapsed = int((time.time() - start) * 1000)

        if result.returncode == 0 and content and not is_blocked(content):
            return FetchResult(
                url=url, content=content, level_used=1,
                level_name=LEVEL_NAMES[1], elapsed_ms=elapsed, success=True
            )
        return FetchResult(
            url=url, content="", level_used=1, level_name=LEVEL_NAMES[1],
            elapsed_ms=elapsed, success=False,
            error=f"Blocked or empty. stderr: {result.stderr[:200]}"
        )
    except Exception as e:
        return FetchResult(
            url=url, content="", level_used=1, level_name=LEVEL_NAMES[1],
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error=str(e)
        )


# ─── Level 2: Scrapling Basic ──────────────────────────────────────────────────

def fetch_level2(url: str, config: FetchConfig) -> FetchResult:
    """Level 2: Scrapling Fetcher with randomized headers."""
    start = time.time()
    try:
        from scrapling.fetchers import Fetcher

        ua = random.choice(USER_AGENTS)
        proxy = pick_proxy(config.proxy_mode)

        fetcher = Fetcher(auto_match=True)
        kwargs = {
            "stealthy_headers": True,
            "follow_redirects": True,
            "timeout": config.timeout_ms / 1000,
        }
        if proxy:
            kwargs["proxy"] = proxy

        if config.human_path:
            homepage = get_homepage_url(url)
            if homepage != url:
                if config.verbose:
                    print(f"  [human-path] Warming via {homepage}")
                try:
                    fetcher.get(homepage, **kwargs)
                    jitter_sleep(1.0, 3.0)
                except Exception:
                    pass

        response = fetcher.get(url, **kwargs)
        elapsed = int((time.time() - start) * 1000)

        content = response.markdown if hasattr(response, "markdown") else response.text
        status = response.status

        if is_blocked(content, status):
            return FetchResult(
                url=url, content="", level_used=2, level_name=LEVEL_NAMES[2],
                elapsed_ms=elapsed, status_code=status, success=False,
                error="Blocked by WAF/bot detection", proxy_used=proxy
            )

        title = None
        try:
            title_el = response.css("title")
            if title_el:
                title = title_el[0].text
        except Exception:
            pass

        return FetchResult(
            url=url, content=content, level_used=2, level_name=LEVEL_NAMES[2],
            elapsed_ms=elapsed, status_code=status, title=title,
            success=True, proxy_used=proxy
        )
    except ImportError:
        return FetchResult(
            url=url, content="", level_used=2, level_name=LEVEL_NAMES[2],
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error="scrapling not installed. Run: pip install scrapling"
        )
    except Exception as e:
        return FetchResult(
            url=url, content="", level_used=2, level_name=LEVEL_NAMES[2],
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error=str(e)
        )


# ─── Level 3: Firecrawl / Browserless ─────────────────────────────────────────

def fetch_level3_firecrawl(url: str, config: FetchConfig) -> FetchResult:
    """Level 3a: Firecrawl cloud scraper."""
    start = time.time()
    try:
        import urllib.request
        api_key = os.environ.get("FIRECRAWL_API_KEY", "")
        if not api_key:
            return FetchResult(
                url=url, content="", level_used=3, level_name="Firecrawl",
                elapsed_ms=0, success=False, error="No FIRECRAWL_API_KEY"
            )

        payload = json.dumps({
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "timeout": 30000,
        }).encode()

        req = urllib.request.Request(
            "https://api.firecrawl.dev/v1/scrape",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read())

        elapsed = int((time.time() - start) * 1000)
        content = data.get("data", {}).get("markdown", "") or data.get("data", {}).get("content", "")
        title = data.get("data", {}).get("metadata", {}).get("title")

        if not content or is_blocked(content):
            return FetchResult(
                url=url, content="", level_used=3, level_name="Firecrawl",
                elapsed_ms=elapsed, success=False, error="Empty or blocked response"
            )

        return FetchResult(
            url=url, content=content, level_used=3, level_name="Firecrawl",
            elapsed_ms=elapsed, title=title, success=True
        )
    except Exception as e:
        return FetchResult(
            url=url, content="", level_used=3, level_name="Firecrawl",
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error=str(e)
        )


def fetch_level3_browserless(url: str, config: FetchConfig) -> FetchResult:
    """Level 3b: Browserless CDP browser."""
    start = time.time()
    try:
        import urllib.request
        api_key = os.environ.get("BROWSERLESS_API_KEY", "")
        if not api_key:
            return FetchResult(
                url=url, content="", level_used=3, level_name="Browserless",
                elapsed_ms=0, success=False, error="No BROWSERLESS_API_KEY"
            )

        wait_selector = None
        domain = urllib.parse.urlparse(url).netloc
        if "twitter.com" in domain or "x.com" in domain:
            wait_selector = '[data-testid="tweetText"]'
        elif "linkedin.com" in domain:
            wait_selector = ".feed-shared-update-v2"

        payload_dict = {
            "url": url,
            "gotoOptions": {"waitUntil": "networkidle2", "timeout": 30000},
        }
        if wait_selector:
            payload_dict["waitForSelector"] = {
                "selector": wait_selector,
                "timeout": 10000
            }
            payload_dict["elements"] = [{"selector": wait_selector}]

        payload = json.dumps(payload_dict).encode()
        req = urllib.request.Request(
            f"https://chrome.browserless.io/content?token={api_key}",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=45) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        elapsed = int((time.time() - start) * 1000)

        if is_blocked(html):
            return FetchResult(
                url=url, content="", level_used=3, level_name="Browserless",
                elapsed_ms=elapsed, success=False, error="Blocked response"
            )

        content = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
        content = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL)
        content = re.sub(r"<[^>]+>", " ", content)
        content = re.sub(r"\s+", " ", content).strip()

        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else None

        return FetchResult(
            url=url, content=content, level_used=3, level_name="Browserless",
            elapsed_ms=elapsed, title=title, success=True
        )
    except Exception as e:
        return FetchResult(
            url=url, content="", level_used=3, level_name="Browserless",
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error=str(e)
        )


def fetch_level3(url: str, config: FetchConfig) -> FetchResult:
    """Level 3: Try Firecrawl first, then Browserless."""
    result = fetch_level3_firecrawl(url, config)
    if result.success:
        return result
    if config.verbose:
        print(f"  Firecrawl failed: {result.error}. Trying Browserless...")
    return fetch_level3_browserless(url, config)


# ─── Level 4: Scrapling Stealth + Mobile Proxy ────────────────────────────────

def fetch_level4(url: str, config: FetchConfig) -> FetchResult:
    """Level 4: StealthyFetcher + Cloudflare solver + Mobile proxy. The nuke."""
    start = time.time()
    try:
        from scrapling.fetchers import StealthyFetcher

        effective_mode = "mobile" if config.proxy_mode in ("mobile", "none") else config.proxy_mode
        proxy_url = pick_proxy(effective_mode)
        if not proxy_url and config.proxy_mode == "none":
            proxy_url = pick_proxy("residential")

        proxy_dict = proxy_to_scrapling(proxy_url) if proxy_url else None

        if config.verbose and proxy_url:
            safe_proxy = proxy_url.split("@")[-1] if "@" in proxy_url else proxy_url
            print(f"  [L4] Using proxy: ...@{safe_proxy}")

        fetcher_kwargs = {
            "solve_cloudflare": True,
            "headless": True,
            "disable_resources": False,
            "hide_canvas": True,
            "block_webrtc": True,
            "google_search": True,
            "timeout": config.timeout_ms,
            "network_idle": True,
        }
        if proxy_dict:
            fetcher_kwargs["proxy"] = proxy_dict

        if config.human_path:
            homepage = get_homepage_url(url)
            if homepage != url:
                if config.verbose:
                    print(f"  [L4 human-path] Visiting homepage: {homepage}")
                try:
                    home_kwargs = dict(fetcher_kwargs)
                    home_kwargs["wait"] = random.randint(1500, 3500)
                    StealthyFetcher.fetch(homepage, **home_kwargs)
                    delay = jitter_sleep(config.jitter_min, config.jitter_max)
                    if config.verbose:
                        print(f"  [L4 human-path] Waited {delay:.1f}s")
                except Exception as e:
                    if config.verbose:
                        print(f"  [L4 human-path] Homepage fetch failed (ok): {e}")

        fetcher_kwargs["wait"] = random.randint(2000, 5000)

        if config.selector:
            fetcher_kwargs["wait_selector"] = config.selector

        response = StealthyFetcher.fetch(url, **fetcher_kwargs)
        elapsed = int((time.time() - start) * 1000)

        content = ""
        if hasattr(response, "markdown") and response.markdown:
            content = response.markdown
        elif hasattr(response, "text"):
            content = response.text

        status = getattr(response, "status", None)

        if is_blocked(content, status):
            return FetchResult(
                url=url, content="", level_used=4, level_name=LEVEL_NAMES[4],
                elapsed_ms=elapsed, status_code=status, success=False,
                error="Still blocked even at L4", proxy_used=proxy_url
            )

        title = None
        try:
            title_el = response.css("title")
            if title_el:
                title = title_el[0].text
        except Exception:
            pass

        if config.selector:
            try:
                elements = response.css(config.selector)
                if elements:
                    content = "\n".join(el.text for el in elements)
            except Exception:
                pass

        return FetchResult(
            url=url, content=content, level_used=4, level_name=LEVEL_NAMES[4],
            elapsed_ms=elapsed, status_code=status, title=title,
            success=True, proxy_used=proxy_url
        )
    except ImportError:
        return FetchResult(
            url=url, content="", level_used=4, level_name=LEVEL_NAMES[4],
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error="scrapling not installed. Run: pip install scrapling"
        )
    except Exception as e:
        return FetchResult(
            url=url, content="", level_used=4, level_name=LEVEL_NAMES[4],
            elapsed_ms=int((time.time() - start) * 1000),
            success=False, error=str(e)
        )


# ─── Main Orchestrator ─────────────────────────────────────────────────────────

class StealthFetcher:
    """
    No Mercy Fetching Engine.
    Auto-escalates through 4 levels until content is extracted.
    """

    def __init__(
        self,
        proxy_mode: str = "none",
        start_level: int = 1,
        max_level: int = 4,
        human_path: bool = False,
        selector: Optional[str] = None,
        timeout_ms: int = 30000,
        jitter_min: float = 1.5,
        jitter_max: float = 6.0,
        verbose: bool = True,
    ):
        self.config = FetchConfig(
            proxy_mode=proxy_mode,
            start_level=start_level,
            max_level=max_level,
            human_path=human_path,
            selector=selector,
            timeout_ms=timeout_ms,
            jitter_min=jitter_min,
            jitter_max=jitter_max,
            verbose=verbose,
        )
        self._level_fns = {
            1: fetch_level1,
            2: fetch_level2,
            3: fetch_level3,
            4: fetch_level4,
        }

    def fetch(self, url: str) -> FetchResult:
        """Fetch URL, escalating through levels until success or exhaustion."""
        if self.config.verbose:
            print(f"\n[StealthFetcher] Target: {url}")
            print(f"  Proxy mode: {self.config.proxy_mode} | Human-path: {self.config.human_path}")
            print(f"  Starting at Level {self.config.start_level}, max Level {self.config.max_level}\n")

        last_result = None
        for level in range(self.config.start_level, self.config.max_level + 1):
            level_name = LEVEL_NAMES.get(level, f"Level {level}")
            if self.config.verbose:
                print(f"[L{level}] {level_name}...")

            result = self._level_fns[level](url, self.config)

            if result.success:
                if self.config.verbose:
                    print(f"[L{level}] SUCCESS in {result.elapsed_ms}ms")
                    if result.title:
                        print(f"  Title: {result.title}")
                    print(f"  Content: {len(result.content)} chars")
                return result

            if self.config.verbose:
                print(f"[L{level}] FAILED: {result.error}")

            last_result = result

            if level < self.config.max_level:
                delay = jitter_sleep(self.config.jitter_min, self.config.jitter_max)
                if self.config.verbose:
                    print(f"  Waiting {delay:.1f}s before escalating...\n")

        if self.config.verbose:
            print(f"\n[StealthFetcher] All levels exhausted. Target is truly fortified.")

        if last_result:
            last_result.success = False
            last_result.error = "All levels failed"
            return last_result

        return FetchResult(
            url=url, content="", level_used=0, level_name="None",
            success=False, error="All levels failed"
        )


# ─── CLI Entry Point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Stealth Fetch — No Mercy Web Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 stealth_fetch.py "https://bloomberg.com/article/xyz"
  python3 stealth_fetch.py "https://x.com/user" --proxy mobile --human-path
  python3 stealth_fetch.py "https://ft.com/article" --start-level 3
  python3 stealth_fetch.py "https://example.com" --selector "article.body" --json
        """
    )
    parser.add_argument("url", help="Target URL to fetch")
    parser.add_argument(
        "--proxy", choices=["none", "residential", "mobile"],
        default="none", help="Proxy mode (default: none)"
    )
    parser.add_argument(
        "--start-level", type=int, choices=[1, 2, 3, 4],
        default=1, help="Start escalation at this level (default: 1)"
    )
    parser.add_argument(
        "--max-level", type=int, choices=[1, 2, 3, 4],
        default=4, help="Maximum escalation level (default: 4)"
    )
    parser.add_argument(
        "--human-path", action="store_true",
        help="Visit homepage first to warm cookies"
    )
    parser.add_argument(
        "--selector", help="CSS selector to extract specific content"
    )
    parser.add_argument(
        "--timeout", type=int, default=30000,
        help="Timeout in milliseconds (default: 30000)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--output", help="Save content to this file path"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    fetcher = StealthFetcher(
        proxy_mode=args.proxy,
        start_level=args.start_level,
        max_level=args.max_level,
        human_path=args.human_path,
        selector=args.selector,
        timeout_ms=args.timeout,
        verbose=not args.quiet,
    )

    result = fetcher.fetch(args.url)

    if args.json:
        output = {
            "url": result.url,
            "success": result.success,
            "level_used": result.level_used,
            "level_name": result.level_name,
            "title": result.title,
            "elapsed_ms": result.elapsed_ms,
            "status_code": result.status_code,
            "proxy_used": result.proxy_used,
            "error": result.error,
            "content_length": len(result.content),
            "content": result.content,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 60)
        print(f"Result: {'SUCCESS' if result.success else 'FAILED'}")
        print(f"Level used: {result.level_used} ({result.level_name})")
        if result.title:
            print(f"Title: {result.title}")
        print(f"Content length: {len(result.content)} chars")
        print(f"Elapsed: {result.elapsed_ms}ms")
        if result.error:
            print(f"Error: {result.error}")
        print("=" * 60)
        if result.content:
            print("\n--- CONTENT ---\n")
            print(result.content[:5000])
            if len(result.content) > 5000:
                print(f"\n... [{len(result.content) - 5000} more chars]")

    if args.output and result.content:
        Path(args.output).write_text(result.content, encoding="utf-8")
        if not args.quiet:
            print(f"\nSaved to: {args.output}")

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
