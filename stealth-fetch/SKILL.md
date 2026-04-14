---
name: stealth-fetch
description: "Use this skill when scraping difficult or bot-protected websites. Trigger on 'scrape this site', 'bypass Cloudflare', 'web scraping', 'site is blocking me', 'nuke fetch'."
---

# Stealth Fetch

**"The nuclear option."**

When everything else has failed, this is your last resort. An automated escalation engine that goes from polite markdown fetcher to full Cloudflare-busting stealth browser with mobile proxy rotation. It does not stop. It does not give up. It gets the data.

## When to Use

- `web_fetch` returned blocked/403/captcha
- Firecrawl returned partial or empty content
- Site uses Cloudflare, DataDome, PerimeterX, or similar WAF
- JS-heavy SPA that blocks bots
- X/Twitter, LinkedIn, Bloomberg, FT, NYT, etc.
- Any time you need guaranteed content extraction from a hostile site

## Trigger Phrases

- "scrape this site aggressively"
- "try harder to fetch this"
- "use no mercy mode"
- "use the nuclear option"
- "all other fetchers failed"
- "bypass cloudflare"

## The Escalation Ladder

```
Level 1 → Level 2 → Level 3 → Level 4
  Fast         Smart      Cloud      Stealth+Proxy
```

### Level 1: Markdown Fetcher (Fast, Free)
- Uses a local `fetch-markdown.sh` Cloudflare worker script
- Fastest, no fingerprint risk, ~80% fewer tokens
- Falls through on: 403, 429, empty body, Cloudflare JS challenge page

### Level 2: Scrapling Basic (`Fetcher`)
- Direct HTTP requests with randomized headers + fingerprints
- User-agent rotation from a real browser pool
- Referer spoofing (Google search origin)
- Falls through on: WAF block, CAPTCHA, JS requirement

### Level 3: Firecrawl / Browserless.io (Cloud Rendering)
- Firecrawl: headless cloud browser, returns clean markdown
- Browserless: full CDP browser, can wait for selectors
- Supports `waitForSelector`, cookie injection
- Falls through on: site-level API ban, persistent fingerprint block

### Level 4: Scrapling Stealth + Mobile Proxy (The Nuke)
- `StealthyFetcher` with `solve_cloudflare=True`
- Mobile proxy rotation (real 4G/5G IPs)
- Canvas noise injection, WebRTC blocking
- Human-path mode: fetches homepage first to warm cookies
- Jittered delays between requests (2-8s random)
- Full fingerprint randomization per request

## Proxy Strategy

| Mode        | Provider    | Best For                              |
|-------------|-------------|---------------------------------------|
| residential | Webshare    | General scraping, news sites          |
| mobile      | Decodo      | X/Twitter, LinkedIn, high-security    |
| none        | Direct      | Level 1-2 only, public content        |

Proxy rotation is automatic. Each request picks a different proxy from the pool.

## Usage

```bash
# Basic: auto-escalate until success
python3 scripts/stealth_fetch.py "https://example.com/article"

# With proxy mode
python3 scripts/stealth_fetch.py "https://twitter.com/user" --proxy mobile

# Human-path mode (warm cookies via homepage first)
python3 scripts/stealth_fetch.py "https://bloomberg.com/article" --human-path

# Start at a specific level
python3 scripts/stealth_fetch.py "https://ft.com/article" --start-level 3

# Extract specific selector
python3 scripts/stealth_fetch.py "https://example.com" --selector "article.content"

# Output as JSON
python3 scripts/stealth_fetch.py "https://example.com" --json

# Save to file
python3 scripts/stealth_fetch.py "https://example.com" --output /tmp/result.md
```

## Python API

```python
from skills.stealth_fetch.scripts.stealth_fetch import StealthFetcher

fetcher = StealthFetcher(proxy_mode="mobile", human_path=True)
result = fetcher.fetch("https://bloomberg.com/article/xyz")

print(result.content)     # Extracted text/markdown
print(result.level_used)  # Which level succeeded (1-4)
print(result.url)         # Final URL (after redirects)
```

## Environment Variables

```
FIRECRAWL_API_KEY=...          # Optional but recommended
BROWSERLESS_API_KEY=...        # Optional
DECODO_MOBILE_PROXY=...        # Optional - format: http://user:pass@gate.decodo.com:10001
WEBSHARE_PROXY_LIST=...       # Optional - path to proxy file
FETCH_MARKDOWN_SCRIPT=...      # Optional - path to fetch-markdown.sh (default: look in common paths)
```

## Adaptive Parsing

Scrapling's auto-relocation engine means even if a site redesigns its HTML structure, the parser will find the content by semantic similarity. No need to update CSS selectors after site changes.

## Anti-Detection Techniques

1. **Header randomization**: Rotates Accept-Language, Accept-Encoding, Sec-Fetch-* headers
2. **User-agent rotation**: Real Chrome/Firefox/Safari UAs, version-matched
3. **Jittered delays**: Random 2-8s between requests (human rhythm)
4. **Canvas noise**: Random perturbation prevents canvas fingerprinting
5. **WebRTC blocking**: Prevents local IP leak through WebRTC
6. **Google referer**: Mimics organic search traffic
7. **Human-path mode**: Visits homepage/sitemap before target URL
8. **Mobile proxy**: Real mobile IPs defeat residential proxy blacklists

## Notes

- Level 4 is slow (10-30s per request). Use only when needed.
- Mobile proxy costs ~$4/GB. Be mindful of large media downloads.
- Firecrawl has a rate limit on the free tier. Monitor usage.
- Never run Level 4 in a tight loop. Use jitter. Be human.
