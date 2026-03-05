---
name: norikae-guide
description: Plan Japan train routes with Yahoo! 乗換案内 and fetch real result content from the website (not MCP). Use when users ask for station-to-station routing in Japan, need natural language constraints mapped to 乗換案内 options, want route details extracted from the result page, or provide English/Chinese station names that must be converted to Japanese station names.
---

# Norikae Guide

## Workflow

1. Normalize station names to Japanese station names used by Yahoo! 乗換案内.
- Convert English/Chinese names before querying.
- If a station is ambiguous, ask one clarification question.

2. Convert user intent into canonical fields.
- Required fields: `from`, `to`
- Optional fields: `via` (max 3), `year`, `month`, `day`, `hour`, `minute`
- Preference fields: `timeType`, `ticket`, `seatPreference`, `walkSpeed`, `sortBy`, and transport toggles

3. Fetch route content from Yahoo Transit.
- Prefer `python3 scripts/fetch_norikae_routes.py --from ... --to ... --show-url`.
- If URL already exists, use `python3 scripts/fetch_norikae_routes.py --url '<url>' --show-url`.
- Use `--format html` only when structured HTML snippets are needed; default `text` for summaries.

4. Handle fallback paths.
- If fetching fails due network/sandbox issues, still provide the generated URL and state that live fetch is unavailable.
- If date/time is missing, default to current local time.
- If constraints conflict (for example "fastest" and "cheapest"), ask which one has priority.

5. Return concise output.
- Include the final URL.
- Include extracted route content or a summarized version.
- Include interpreted fields (especially normalized Japanese station names).

## Canonical Fields

| Field | Type | Notes |
| --- | --- | --- |
| `from` | string | Departure station in Japanese |
| `to` | string | Arrival station in Japanese |
| `via` | string[] | Up to 3 via stations; ignore extras |
| `year` `month` `day` | number | Travel date |
| `hour` `minute` | number | Travel time |
| `timeType` | enum | `departure`, `arrival`, `first_train`, `last_train`, `unspecified` |
| `ticket` | enum | `ic`, `cash` |
| `seatPreference` | enum | `non_reserved`, `reserved`, `green` |
| `walkSpeed` | enum | `fast`, `slightly_fast`, `slightly_slow`, `slow` |
| `sortBy` | enum | `time`, `transfer`, `fare` |
| `useAirline` etc. | boolean | Transport include/exclude toggles |

## Default Heuristics

- Map "最便宜 / cheapest" to `sortBy=fare`.
- Map "换乘最少 / fewest transfers" to `sortBy=transfer`.
- Map "不用新干线 / no shinkansen" to `useShinkansen=false`.
- Keep `ticket=ic`, `seatPreference=non_reserved`, `walkSpeed=slightly_slow` unless user overrides.

## Resources

- Parameter reference: [references/yahoo-transit-params.md](references/yahoo-transit-params.md)
- URL builder script: `scripts/build_norikae_url.py`
- Fetch + extractor script: `scripts/fetch_norikae_routes.py`

Use the fetch script by default when route content is requested.
