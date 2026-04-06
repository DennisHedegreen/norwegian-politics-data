# Methodology — Norwegian Politics Data

## What this tool is

A private Norway-only deploy mirror for internal reading and staging. It pairs the current Storting election bridge-safe municipality layer with the narrow factor set that is honest enough to render now, without pretending the Norway surface is public-ready.

## What this tool is not

- It is not a prediction model.
- It is not a political recommendation engine.
- Correlation is not causation.
- Municipal-level patterns do not describe individual voters.

## Mirror scope

- Country: `Norway`
- Election type: `Storting`
- Public geography: `municipality`
- Public geography count: `357`
- Current public factors: `Population, Population density, Age 65+, Turnout, Cars, Income, Education`

## Data handling rules

- Missing data is shown honestly rather than backfilled.
- Public factors only enter the surface when municipality coverage and semantics are good enough.
- Party label mode only changes displayed labels. Data values and party IDs remain the same.
- The public layer stays narrower than the internal engine on purpose.

## Sources

- Election source: `Statistics Norway Storting municipality bridge-safe layer + factor harvests`
- Secondary source: `Valgdirektoratet partial territorial notes stay internal-only`
- Statistics source: `Statistics Norway`

## Known limitations

- This surface intentionally keeps a narrower public scope than the internal engine.
- If a factor or year combination does not hold up, it should disappear rather than survive as a lie.
- Some future country-specific factors may exist internally before they earn public release here.
