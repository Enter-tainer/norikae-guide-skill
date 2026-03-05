#!/usr/bin/env python3
"""Fetch and extract Yahoo! 乗換案内 route content."""

from __future__ import annotations

import argparse
from datetime import datetime
import html as html_lib
import re
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://transit.yahoo.co.jp/search/result"

TIME_TYPE_MAP = {
    "departure": "1",
    "arrival": "4",
    "first_train": "3",
    "last_train": "2",
    "unspecified": "5",
}

TICKET_MAP = {
    "ic": "ic",
    "cash": "normal",
}

SEAT_MAP = {
    "non_reserved": "1",
    "reserved": "2",
    "green": "3",
}

WALK_MAP = {
    "fast": "1",
    "slightly_fast": "2",
    "slightly_slow": "3",
    "slow": "4",
}

SORT_MAP = {
    "time": "0",
    "fare": "1",
    "transfer": "2",
}


def build_url(args: argparse.Namespace) -> str:
    now = datetime.now()
    year = args.year if args.year is not None else now.year
    month = args.month if args.month is not None else now.month
    day = args.day if args.day is not None else now.day
    hour = args.hour if args.hour is not None else now.hour
    minute = args.minute if args.minute is not None else now.minute

    via = (args.via or [])[:3]

    params: list[tuple[str, str]] = [
        ("from", args.departure),
        ("to", args.arrival),
        ("y", str(year)),
        ("m", f"{month:02d}"),
        ("d", f"{day:02d}"),
        ("hh", str(hour)),
        ("m1", str(minute // 10)),
        ("m2", str(minute % 10)),
        ("type", TIME_TYPE_MAP[args.time_type]),
        ("ticket", TICKET_MAP[args.ticket]),
        ("expkind", SEAT_MAP[args.seat_preference]),
        ("ws", WALK_MAP[args.walk_speed]),
        ("s", SORT_MAP[args.sort_by]),
        ("al", "1" if args.use_airline else "0"),
        ("shin", "1" if args.use_shinkansen else "0"),
        ("ex", "1" if args.use_express else "0"),
        ("hb", "1" if args.use_highway_bus else "0"),
        ("lb", "1" if args.use_local_bus else "0"),
        ("sr", "1" if args.use_ferry else "0"),
    ]

    for station in via:
        params.append(("via", station))

    return f"{BASE_URL}?{urlencode(params)}"


def fetch_html(url: str, timeout: int) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="ignore")


def strip_noise(html: str) -> str:
    cleaned = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
    cleaned = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<!--[\s\S]*?-->", "", cleaned)
    cleaned = re.sub(r"<nav[^>]*>[\s\S]*?</nav>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<header[^>]*>[\s\S]*?</header>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<footer[^>]*>[\s\S]*?</footer>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<aside[^>]*>[\s\S]*?</aside>", "", cleaned, flags=re.IGNORECASE)
    return cleaned


def html_to_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "\n", fragment)
    text = html_lib.unescape(text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract_content(html: str, output_format: str) -> str:
    cleaned = strip_noise(html)

    route_start_match = re.search(
        r'(<div[^>]*class="[^"]*routeDetail[^"]*"[^>]*>)',
        cleaned,
        flags=re.IGNORECASE,
    )
    route_end = cleaned.find("条件を変更して検索")

    if route_start_match and route_end != -1 and route_end > route_start_match.start():
        section = cleaned[route_start_match.start():route_end]
        return section.strip() if output_format == "html" else html_to_text(section)

    text = html_to_text(cleaned)
    text_start = text.find("ルート1")
    text_end = text.find("条件を変更して検索")

    if text_start != -1 and text_end != -1 and text_end > text_start:
        text = text[text_start:text_end]

    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch and extract route details from Yahoo! 乗換案内."
    )

    parser.add_argument("--url", help="Fully prepared Yahoo transit URL")
    parser.add_argument("--from", dest="departure", help="Departure station in Japanese")
    parser.add_argument("--to", dest="arrival", help="Arrival station in Japanese")
    parser.add_argument("--via", action="append", help="Via station (repeatable, max 3)")

    parser.add_argument("--year", type=int)
    parser.add_argument("--month", type=int)
    parser.add_argument("--day", type=int)
    parser.add_argument("--hour", type=int)
    parser.add_argument("--minute", type=int)

    parser.add_argument(
        "--time-type",
        default="departure",
        choices=sorted(TIME_TYPE_MAP.keys()),
    )
    parser.add_argument(
        "--ticket",
        default="ic",
        choices=sorted(TICKET_MAP.keys()),
    )
    parser.add_argument(
        "--seat-preference",
        default="non_reserved",
        choices=sorted(SEAT_MAP.keys()),
    )
    parser.add_argument(
        "--walk-speed",
        default="slightly_slow",
        choices=sorted(WALK_MAP.keys()),
    )
    parser.add_argument(
        "--sort-by",
        default="time",
        choices=sorted(SORT_MAP.keys()),
    )

    parser.add_argument("--use-airline", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--use-shinkansen", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--use-express", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--use-highway-bus", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--use-local-bus", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--use-ferry", action=argparse.BooleanOptionalAction, default=True)

    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--format", choices=["text", "html"], default="text")
    parser.add_argument("--show-url", action="store_true")

    args = parser.parse_args()

    if not args.url and (not args.departure or not args.arrival):
        parser.error("Provide --url, or both --from and --to.")

    return args


def main() -> int:
    args = parse_args()
    url = args.url or build_url(args)

    try:
        html = fetch_html(url, args.timeout)
        content = extract_content(html, args.format)
    except Exception as exc:  # pragma: no cover - network/runtime failures
        print(f"Error fetching route data: {exc}", file=sys.stderr)
        return 1

    if args.show_url:
        print(f"URL: {url}")
        print()

    print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
