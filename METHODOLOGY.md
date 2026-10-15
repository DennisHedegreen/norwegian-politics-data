# Norway methodology

The app computes Pearson correlations between party vote share and a selected municipality factor. It reports the number of matched municipalities. Thin-coverage parties may have fewer observations; the default party filter limits their influence.

## Municipality geography

The 2025 Storting layer covers all 357 municipalities on current codes. The 2021 layer is mapped through direct municipality identities to 355 current codes. Old Ålesund (1507) cannot be divided reliably between current Ålesund (1508) and Haram (1580), because pooled advance votes cannot be allocated to the two territories. Both current targets are excluded from 2021 municipality analysis; no weights or partial Haram results are substituted. The reviewed mapping is included in norway/geography/municipality_bridge_2021_to_current.csv.

Factors use the current municipality code to align display names with the election layer. Original source spelling is retained in source_municipality where a factor file needs a name alignment. This fixes Fauske's differing Sami spellings without changing its values or identity.

## Factor measurements

| Factor | Source and measurement | Election picker |
|---|---|---|
| Population | SSB 11342, residents on 1 January | 2025 |
| Population density | SSB 11342, residents per km² of land | 2025 |
| Age 65+ | SSB 07459, ages 65–105+, divided by same-year population | 2025 |
| Turnout | SSB 08243, Storting turnout in the election year | 2021 and 2025 |
| Cars | SSB 07849 private passenger cars / SSB 11342 population × 1,000 | 2025 |
| Education | SSB 09429 short + long higher education, ages 16+, levels 03a + 04a, all sexes | 2025 |

Education excludes tertiary vocational level 11. From 2025, leased vehicles with registered lessees are assigned to lessees' municipalities instead of owners' municipalities. Cars is therefore a 2025 structural indicator here; earlier vehicle years are not exposed as a comparable trend. Population is measured on 1 January, while the registered-vehicle stock is measured at year end; the car ratio is a structural indicator, not a same-day count. SSB's private-car vehicle category also includes ambulances, combined vehicles and motorhomes; it is not a count of exclusively personally owned cars. See [SSB's registered-vehicle definitions](https://www.ssb.no/en/transport-og-reiseliv/landtransport/statistikk/bilparken).

Population, density and age data for 2024/2026, education 2024 and income 2024 remain labelled context in the package. They are not relabelled as 2025 measurements or offered as extra election years. Income is median ordinary income after special deduction for residents aged 17+, SSB 05671, and remains outside the factor picker.

## National results and interpretation

National trends use SSB 08092's national totals, not an average of municipality shares and not the 355-municipality subset. Correlation is not causation. Municipality-level findings cannot establish individual voters' characteristics or reasons for voting. A missing result is not zero, and original party identities remain unchanged by the label language.

## Source verification

The candidate replays captured official SSB responses and compares all numerical values with the accepted engine data. Capture dates, exact query URLs and SHA-256 hashes are recorded in the public-safe provenance manifest. Raw responses are retained in the canonical source archive, rather than duplicated in this package. There is no incomplete Haram territorial reconstruction in the candidate.
