# Norway Harvest Backlog

First Norway source-lock backlog.

The goal is not to prove Norway is ready.
The goal is to turn "Norway next" into a real harvesting queue with named official source paths.

## Election

### Storting valid votes by party and municipality

Status:

- source locked
- first harvest landed

Current source candidate:

- `SSB Statbank 08092`
  `Storting election. Valid votes, by party/electoral list (M) 1945-2025`

Current first output:

- `norway/storting/storting_party_share_by_municipality.csv`
- `2021` on `2020-2023` election geography
- `2025` on `2024-` election geography
- percentage vote share is sourced directly from `GodkjenteProsent`

Open questions:

- how to handle the remaining `Alesund/Haram` split honestly inside the `2021 -> current` bridge
- whether older municipality-election layers should be harvested before the first normalization rule is written down

### Storting turnout by municipality

Status:

- source locked
- first harvest landed

Current source candidate:

- `SSB Statbank 08243`
  `Storting election. Electoral turnout (per cent) (M) 1945-2025`

Current first outputs:

- `norway/storting/storting_turnout_by_municipality.csv`
- `norway/storting/storting_turnout_by_current_municipality_bridge_safe.csv`
- `norway/factors/turnout_pct.csv`

Current note:

- the public-style factor file still exposes only `2025`
- a bridge-safe current-municipality turnout layer now exists internally for `2021` and `2025`
- the unresolved `Alesund/Haram` split keeps `2021` out of a full current-municipality public-style layer for now

### Votes by validity and time of vote

Status:

- source identified
- not required for the first adapter

Current source candidate:

- `SSB Statbank 11691`
  `Storting election. Votes, by validity and time of vote (M) 1945-2025`

Use:

- backup context
- not first-pass core data

## Factors

### Population and area

Status:

- source locked
- first harvest landed

Current source candidate:

- `SSB Statbank 11342`
  `Population and area (M) 2007-2026`

Use:

- `population`
- `population_density`
- municipality normalization cross-checks

Current first outputs:

- `norway/factors/population.csv`
- `norway/factors/population_density.csv`
- current `2024-2026` factor window on `357` real `2024-` municipality codes
- `9999` unknown municipality is deliberately filtered out

### Income

Status:

- source locked
- first harvest landed

Current source candidate:

- `SSB Statbank 05671`
  `Taxable income, deduction and assessed taxes. Residents 17 years and older. Median (NOK) (M) 1993-2024`

Current first output:

- `norway/factors/income.csv`
- current honest window: `2024`

### Education

Status:

- source locked for first pass
- first harvest landed

Current source candidates:

- `SSB Statbank 09429`

Current first output:

- `norway/factors/education.csv`
- first pass uses `03a` + `04a`
- tertiary vocational `11` is deliberately excluded for now

Open question:

- whether tertiary vocational education should later become part of a Norway-local shadow factor or of the mapped family

### Age structure

Status:

- source locked
- first harvest landed

Current source path:

- `SSB Statbank 07459`
  `Population, by sex and one-year age groups (M) 1986-2026`

Current first output:

- `norway/factors/age65_pct.csv`
- current honest window: `2024-2026`

## Geometry / entity language

### Municipality reform handling

Status:

- major semantic blocker

Need:

- explicit normalization rule for municipality reforms
- documentation of which elections can be mapped honestly to current municipality IDs
- a named resolution strategy for the `2021` `Alesund/Haram` split that still survives after the first bridge-safe current layer

## Rule

If the first Norway source pass produces a fake-simple answer, stop and document the problem before building a public layer on top of it.
