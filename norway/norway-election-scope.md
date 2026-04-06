# Norway Election Scope

Working target for the first Norway election layer:

- election type: `Storting`
- public geography target: `municipality`
- primary source candidates:
  - `Statistics Norway (SSB)` Statbank Storting tables
  - `Valgdirektoratet / valgresultat.no` official result surface

Why this is the right first Norway scope:

- national parliamentary election is the cleanest first political layer
- municipality-level reading matches the current Denmark and Sweden public shape
- official Norway statistics already expose Storting voting tables with municipality-level outputs

First internal decision to lock:

- whether the first normalized municipality layer should start at `2021` and `2025`
- or whether `2013`, `2017`, `2021`, and `2025` can be made honest under one municipality schema

Important Norway-specific risk:

- Norway municipality boundaries have changed repeatedly
- SSB exposes multiple municipality classifications across time
- the first Norway layer should not pretend older election years are directly comparable until the normalization rule is explicit

Not in scope yet:

- local elections
- county-level public release
- Norway-vs-Denmark or Norway-vs-Sweden public comparison
- any public Norway release repo
