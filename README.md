# Norwegian Politics Data

Approved public-preview release for municipality-level Storting patterns. Deployment and live verification are pending. The GitHub source mirror remains private; its history has not been made public.

## Scope

- 2025: all 357 municipalities; population, population density, age 65+, turnout, cars and education.
- 2021: turnout only across 355 current municipalities; Ålesund and Haram are excluded.
- National trends: full-country official vote shares for 2021 and 2025.
- Native, English and Both party labels. Income 2024 remains labelled context, outside the factor picker.

Correlation is not causation. Municipality patterns do not describe individual voters. Read [METHODOLOGY.md](METHODOLOGY.md) and the included [source manifest](provenance/norway_release_candidate_manifest.json).

## Run locally

```sh
pip install -r requirements.txt
streamlit run app.py
```

The app has Explore, By Municipality, National trends and About & sources. World-politics-data is the canonical source; this is a generated deploy mirror.
