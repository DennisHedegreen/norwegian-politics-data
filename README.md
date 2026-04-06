# Norwegian Politics Data

A private Norway-only deploy mirror for the current bridge-safe Storting municipality layer, kept internal until the Norway surface is honest enough for public release.

This repo is the Norway-only private mirror extracted from the internal World-politics-data engine. It keeps the Norway app shell, Norway data pack, bridge notes, and internal-only scope docs without pretending that Norway is already public-ready.

## Internal status

- Mirror visibility: `private`
- Public launch status: `not public-ready`
- GitHub repo: `https://github.com/DennisHedegreen/norwegian-politics-data`

## Current scope

- Election type: `Storting`
- Bridge-safe municipality election years: `2021`, `2025`
- National trend years: `2021`, `2025`
- Mirror geography: `current municipality`
- Current live factors in the private shell: `population`, `population density`, `age65`, `turnout`

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What this repo is not

- Not a public launch
- Not a claim that the full `2021 -> current` municipality reform problem is solved
- Not a second source of truth beside `World-politics-data`
- Not a full Norway factor release

## Intentionally missing

- `TID` public door and public website links
- Public Streamlit deployment until Norway is explicitly declared public-ready
- `Alesund/Haram` backfill beyond the current explicit internal notes
- Broader Norway factor exposure before the honesty boundary is cleared

## Data sources

- Election source: `Statistics Norway Storting municipality bridge-safe layer + factor harvests`
- Secondary source: `Valgdirektoratet partial territorial notes stay internal-only`
- Statistics source: `Statistics Norway`

## Repo structure

```text
app.py               Single-country private wrapper
engine_app.py        Shared app shell extracted from the internal engine
correlation_utils.py Shared correlation helpers
country_registry.py  Single-country registry for this private mirror
norway/               Country data pack and scope notes
provenance/          Mirror manifests copied from the internal engine
tests/               Country-surface smoke tests
```

## Source of truth

This repo is a private country mirror. It exists to stage and verify Norway as a separate deploy surface while the shared internal engine still remains the only source of truth.
