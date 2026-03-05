# Norikae Guide Skill

A reusable AI skill for Japan transit planning with Yahoo! 乗換案内.

This skill does **not** run an MCP server. Instead, it teaches the agent to:

- map natural-language travel requests to Yahoo transit query parameters
- normalize English/Chinese station names to Japanese station names
- fetch live result pages from `transit.yahoo.co.jp`
- extract route content for downstream summarization

## Install (One Command)

```bash
npx -y skills@latest add Enter-tainer/norikae-guide-skill --skill norikae-guide --yes --global
```

## Skill Contents

- `SKILL.md`: core agent workflow and decision rules
- `references/yahoo-transit-params.md`: full parameter mapping table
- `references/natural-language-examples.md`: natural-language to parameter examples
- `scripts/build_norikae_url.py`: deterministic URL builder
- `scripts/fetch_norikae_routes.py`: live fetch + extraction script

## Local Test

Build URL only:

```bash
python3 scripts/build_norikae_url.py --from 東京 --to 新宿 --hour 10 --minute 30
```

Fetch and extract route content:

```bash
python3 scripts/fetch_norikae_routes.py --from 東京 --to 新宿 --hour 10 --minute 30 --show-url
```

## Notes

- Query station names should be Japanese for reliable results.
- This relies on Yahoo Transit page structure; extraction may need updates if HTML changes.
- Use responsibly and follow the target website terms.
