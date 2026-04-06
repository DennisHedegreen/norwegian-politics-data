# Norway Factor Board

Internal planning note for the first Norway factor passes.

This is not a public comparability claim.
It is a working board for deciding what Norway could add first without lowering the honesty bar.

## First Candidate Public Batch

### `population`

Why:

- core denominator and reference layer
- official municipality table exists in SSB
- needed before several later per-capita or density-style readings can be trusted

Current disposition:

- first harvest landed
- current first window:
  - `2024-2026`
- current source:
  - `SSB table 11342` population and area by municipality

### `population_density`

Why:

- strong first structural signal
- likely derivable from the same population/area family as the core reference layer
- easy public reading

Current disposition:

- first harvest landed
- current first window:
  - `2024-2026`
- current source:
  - `SSB table 11342` population and area by municipality

### `income`

Why:

- likely one of the easiest municipality-safe social indicators to defend first
- already part of the Denmark and Sweden public families

Current disposition:

- first harvest landed
- current first window:
  - `2024`
- current source:
  - `SSB table 05671` median ordinary income after special deduction by municipality

### `education`

Why:

- likely a clean first cross-country family member
- useful structural complement to income

Current disposition:

- first harvest landed
- current first window:
  - `2024`
- current source:
  - `SSB table 09429`
- current first rule:
  - mapped family uses `03a` + `04a`
  - tertiary vocational `11` stays out for now

### `turnout`

Why:

- core election-context signal
- official Storting turnout tables already exist in SSB

Current disposition:

- first harvest landed
- current public-style window:
  - `2025`
- current internal election window:
  - `2021`
  - `2025`
- current bridge-safe current-municipality window:
  - `2021` for `355` current municipalities
  - `2025` for `357` current municipalities
- current source:
  - `SSB table 08243` Storting election turnout by municipality

### `age65`

Why:

- usually one of the cleaner demographic structure signals
- likely easier than labour-market or welfare semantics in a first pass

Current disposition:

- first harvest landed
- current first window:
  - `2024-2026`
- current source:
  - `SSB table 07459`

## Investigate After First Batch

### `cars`

Why:

- could become a useful settlement/rurality complement
- worth testing only after the core population and density path is stable

Current disposition:

- source path audited and ready for a first private-shell pass
- current source:
  - `SSB table 07849` registered vehicles by municipality
- current first rule:
  - use `Private cars` only
  - expose `2025` only
  - normalize as private cars per 1,000 residents against the current population layer
  - keep as `country_local`
  - do not treat `2024 -> 2025` as a clean trend because SSB notes a 2025 placement change for leased vehicles

### `employment` / `unemployment`

Why:

- analytically useful
- but likely more semantically fragile across time and reforms

Current disposition:

- do not prioritize before the first batch is real
- revisit only after the municipality bridge and coverage notes are explicit

### `housing`

Why:

- may become Norway-specific and structurally interesting

Current disposition:

- too early
- only investigate after the first factor family is stable

## Blocked For Now

### `welfare`

Why:

- high semantic drift risk
- likely to become country-local in a way that needs more framing than the first Norway pass should carry

### `crime`

Why:

- source path and public wording are not locked

### `immigration_share`

Why:

- politically and semantically risky
- not a first-pass factor

## Working order

1. keep the explicit municipality bridge between `2020-2023` and `2024-` election geometries truthful
2. decide whether the `Alesund/Haram` split can be resolved from a lower-resolution source or must stay as a named hole
3. decide whether `turnout` can honestly expose `2021` beside `2025` through the bridge-safe current layer
4. keep `cars` as a 2025-only private-shell factor until the leasing-method break is explicitly handled
5. investigate `employment` / `unemployment` only after the bridge edge case is stable
