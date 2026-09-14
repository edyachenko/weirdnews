#!/usr/bin/env python3
"""Scrape PolitiFact fact-checks of Donald Trump (second term, from 2025-01-20).

Run with:
  uv run --project ~/pet-projects/weirdnews/MoneyPrinterTurbo python \
      ~/pet-projects/weirdnews/research/politifact_scrape.py

Writes ~/pet-projects/weirdnews/research/trump_months_raw.json
"""
import json
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "https://www.politifact.com/factchecks/list/page/{page}/?speaker=donald-trump"
BASE_PAGE1 = "https://www.politifact.com/factchecks/list/?speaker=donald-trump"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CUTOFF = date(2025, 1, 1)  # keep scraping until pages are entirely before this
TERM_START = date(2025, 1, 20)
OUT_PATH = Path(__file__).parent / "trump_months_raw.json"

ITEM_RE = re.compile(
    r'stated on (?P<date>\w+ \d{1,2}, \d{4})(?P<ctx>.*?)</span>.*?'
    r'<a href="(?P<url>https://politifact\.com/factchecks/[^"]+)" '
    r'class="pf-statement-quote pf-statement-quote-(?P<ruling>[a-z-]+)[^"]*">'
    r'(?P<quote>.*?)</a>',
    re.DOTALL,
)

TAG_RE = re.compile(r"<[^>]+>")


def clean(s: str) -> str:
    s = TAG_RE.sub("", s)
    s = (s.replace("&#8220;", '"').replace("&#8221;", '"')
           .replace("&#8217;", "'").replace("&#039;", "'")
           .replace("&#8212;", "-").replace("&amp;", "&")
           .replace("&nbsp;", " "))
    return " ".join(s.split()).strip()


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (HTTPError, URLError) as e:
        print(f"  fetch error for {url}: {e}", file=sys.stderr)
        return ""


def parse_page(html: str):
    items = []
    for m in ITEM_RE.finditer(html):
        try:
            d = datetime.strptime(m.group("date"), "%B %d, %Y").date()
        except ValueError:
            continue
        items.append({
            "date": d.isoformat(),
            "ruling": m.group("ruling"),
            "statement": clean(m.group("quote")),
            "url": m.group("url"),
        })
    return items


def main():
    all_items = []
    seen_urls = set()
    page = 1
    consecutive_all_old = 0
    max_pages = 60  # safety cap

    while page <= max_pages:
        url = BASE_PAGE1 if page == 1 else BASE.format(page=page)
        print(f"fetching page {page}: {url}", file=sys.stderr)
        html = fetch(url)
        if not html:
            print(f"  empty response, stopping at page {page}", file=sys.stderr)
            break
        items = parse_page(html)
        if not items:
            print(f"  no items parsed on page {page}, stopping", file=sys.stderr)
            break

        new_count = 0
        for it in items:
            if it["url"] in seen_urls:
                continue
            seen_urls.add(it["url"])
            all_items.append(it)
            new_count += 1

        dates_this_page = [datetime.fromisoformat(it["date"]).date() for it in items]
        max_date = max(dates_this_page)
        min_date = min(dates_this_page)
        any_recent = any(d >= CUTOFF for d in dates_this_page)
        print(f"  {len(items)} items ({new_count} new), range {min_date}..{max_date}, "
              f"any >= {CUTOFF}: {any_recent}", file=sys.stderr)

        if any_recent:
            consecutive_all_old = 0
        else:
            consecutive_all_old += 1
            if consecutive_all_old >= 2:
                print(f"  2 consecutive pages entirely before {CUTOFF}, stopping", file=sys.stderr)
                break

        page += 1
        time.sleep(1)

    # Keep only statements within the second term window
    in_term = [it for it in all_items if it["date"] >= TERM_START.isoformat()]
    in_term.sort(key=lambda x: x["date"])

    print(f"\nTotal scraped (all dates, deduped): {len(all_items)}", file=sys.stderr)
    print(f"In second-term window (>= {TERM_START}): {len(in_term)}", file=sys.stderr)

    OUT_PATH.write_text(json.dumps(in_term, indent=2, ensure_ascii=False))
    print(f"Wrote {OUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
