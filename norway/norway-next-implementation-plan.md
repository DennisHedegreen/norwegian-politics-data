# Norway Next Implementation Plan

Current first harvest landed:

- `norway/` adapter room
- election/factor/boundary notes
- live `fetch_norway.py`
- first SSB factor files
- first internal Storting municipality and national vote files
- first current-municipality bridge-safe election files
- explicit `2021 -> current` municipality bridge table
- provenance manifest
- output contract tests

Next useful passes:

1. decide whether the `Alesund/Haram` split can be resolved from lower-resolution official election material or must stay outside the factor-aware bridge
2. decide whether `2021` turnout can join a public-style current layer as a `355`-municipality constrained year or should stay internal longer
3. add and test `cars` as a private-shell `2025` structural factor from SSB table `07849`
4. investigate whether `employment` or `unemployment` can survive the honesty bar after the bridge work
5. decide whether Norway should stay internal-only for a while after the first pack lands
6. only after the bridge and factor story are honest, add a Norway registry entry and app-shell path

Reference:

- `norway-harvest-backlog.md`
- `norway-factor-board.md`
- `COUNTRY-PRIORITY-NOTES.md`
