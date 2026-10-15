from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from core.correlation import compute_correlation_result, corr_strength_label
from core.presentation import (
    METRIC_SHORT_LABELS,
    render_party_name_selector,
    build_country_finding,
    format_display_table,
    format_party_name,
    render_bar_chart,
    render_compact_dataframe,
    render_country_sidebar_footer,
    render_national_trend_chart,
)


NORWAY_LIVE_FACTOR_KEYS = ("population", "density", "age65", "turnout", "cars", "education")
NORWAY_LIVE_YEARS = (2021, 2025)
NORWAY_DEFAULT_PARTY_MIN_MUNICIPALITIES = 25
NORWAY_DEFAULT_PARTY_MIN_MEAN_SHARE = 0.5
NORWAY_BRIDGE_SAFE_TURNOUT_FILE = "storting_turnout_by_current_municipality_bridge_safe.csv"
NORWAY_METRIC_OPTIONS = [
    ("population", "Population", "Population (reference count)"),
    ("density", "Population density", "Residents per km²"),
    ("age65", "Age 65+", "Share aged 65+ (%)"),
    ("turnout", "Turnout", "Votes cast as share of voters (%)"),
    ("cars", "Cars", "Passenger cars per 1,000 residents"),
    ("education", "Education", "Short + long higher education, aged 16+ (%)"),
]

NORWAY_FACTOR_METHOD_NOTES = {
    "population": "Residents on 1 January of the factor year (SSB 11342).",
    "density": "Residents per km² of land in the factor year (SSB 11342).",
    "age65": "Residents aged 65+ as a share of all residents in the factor year (SSB 07459 / 11342).",
    "turnout": "Storting election turnout in the selected election year (SSB 08243).",
    "cars": "Registered passenger cars at 31 December 2025 per 1,000 residents at 1 January 2025 (SSB 07849 / 11342). SSB's private-car category includes motorhomes, ambulances and combined vehicles. Earlier car years are not a comparable trend because leased-vehicle placement changed in 2025.",
    "education": "2025 short + long higher education, population aged 16+ (SSB 09429, levels 03a + 04a). Tertiary vocational education is excluded.",
}


def available_norway_metric_items(year, factor_frames):
    allowed = {"turnout"} if int(year) == 2021 else set(NORWAY_LIVE_FACTOR_KEYS)
    return [(key, label, metric_label) for key, label, metric_label in NORWAY_METRIC_OPTIONS
            if key in allowed and not _get_metric_series(key, year, factor_frames).empty]


def _factor_file(country_config, filename: str) -> Path:
    return country_config.factor_dir / filename


def _bridge_safe_turnout_file(country_config) -> Path:
    return country_config.factor_dir.parent / "storting" / NORWAY_BRIDGE_SAFE_TURNOUT_FILE


def is_available(country_config, runtime_context) -> bool:
    return country_config.municipal_vote_path.exists() and country_config.factor_dir.exists()


@st.cache_data
def load_bundle(country_config):
    municipal = pd.read_csv(country_config.municipal_vote_path, dtype={"public_geography_id": str})
    municipal["election_year"] = municipal["election_year"].astype(int)
    municipal["share"] = municipal["share"].astype(float)
    current_names = municipal.loc[municipal["election_year"] == 2025, ["public_geography_id", "municipality"]].drop_duplicates()
    if current_names["public_geography_id"].duplicated().any():
        raise ValueError("Norway municipality codes have conflicting display names")
    names_by_id = current_names.set_index("public_geography_id")["municipality"]

    def align_factor_names(frame):
        if frame.empty:
            return frame
        frame = frame.copy()
        frame["public_geography_id"] = frame["public_geography_id"].astype(str).str.zfill(4)
        names = frame["public_geography_id"].map(names_by_id)
        if names.isna().any():
            raise ValueError("Norway factor contains a municipality code outside the current geography")
        if "source_municipality" not in frame:
            frame["source_municipality"] = frame["municipality"]
        frame["municipality"] = names
        return frame

    national = pd.read_csv(country_config.national_vote_path)
    national["election_year"] = national["election_year"].astype(int)
    national["share"] = national["share"].astype(float)

    factor_frames = {}
    for metric_key in country_config.supported_factors:
        filename = f"{metric_key}.csv" if metric_key == "turnout" else None
        if metric_key == "population":
            filename = "population.csv"
        elif metric_key == "density":
            filename = "population_density.csv"
        elif metric_key == "age65":
            filename = "age65_pct.csv"
        elif metric_key == "turnout":
            path = _bridge_safe_turnout_file(country_config)
            frame = pd.read_csv(path, dtype={"public_geography_id": str}) if path.exists() else pd.DataFrame(columns=["municipality", "year", "value"])
            if not frame.empty:
                frame = frame.rename(columns={"election_year": "year"})
                frame["year"] = frame["year"].astype(int)
            factor_frames[metric_key] = align_factor_names(frame)
            continue
        elif metric_key == "income":
            filename = "income.csv"
        elif metric_key == "education":
            filename = "education.csv"
        elif metric_key == "cars":
            filename = "cars_per_1000.csv"
        if filename is None:
            continue
        path = _factor_file(country_config, filename)
        frame = pd.read_csv(path, dtype={"public_geography_id": str}) if path.exists() else pd.DataFrame(columns=["municipality", "year", "value"])
        if not frame.empty and "year" in frame.columns:
            frame["year"] = frame["year"].astype(int)
        factor_frames[metric_key] = align_factor_names(frame)

    return {
        "municipal": municipal,
        "national": national,
        "factor_frames": factor_frames,
    }


def _get_metric_series(metric_key, year, factor_frames):
    frame = factor_frames.get(metric_key, pd.DataFrame())
    if frame.empty:
        return pd.DataFrame(columns=["municipality", "metric"])
    current = frame[frame["year"] == year][["municipality", "value"]].copy()
    if current.empty:
        return pd.DataFrame(columns=["municipality", "metric"])
    current["metric"] = pd.to_numeric(current["value"], errors="coerce")
    return current[["municipality", "metric"]].dropna(subset=["metric"])


def _metric_label(metric_key: str) -> str:
    for key, label, metric_label in NORWAY_METRIC_OPTIONS:
        if key == metric_key:
            return metric_label
    return metric_key


def _party_options(municipal_df, year):
    year_frame = municipal_df[municipal_df["election_year"] == year].copy()
    if year_frame.empty:
        return []
    profiles = get_norway_party_profiles(year_frame)
    return profiles["party"].tolist()


def get_norway_party_profiles(municipal_df):
    if municipal_df.empty:
        return pd.DataFrame(columns=["party", "municipality_count", "mean_share", "default_public"])
    stats = (
        municipal_df[municipal_df["share"] > 0]
        .groupby("party", as_index=False)
        .agg(
            municipality_count=("municipality", "nunique"),
            mean_share=("share", "mean"),
        )
    )
    stats["default_public"] = (
        (stats["municipality_count"] >= NORWAY_DEFAULT_PARTY_MIN_MUNICIPALITIES)
        & (stats["mean_share"] >= NORWAY_DEFAULT_PARTY_MIN_MEAN_SHARE)
    )
    return stats.sort_values(["default_public", "mean_share", "municipality_count"], ascending=[False, False, False]).reset_index(drop=True)


def render(country_config, selected_country_label, runtime_context):
    bundle = load_bundle(country_config)
    municipal = bundle["municipal"]
    national = bundle["national"]
    factor_frames = bundle["factor_frames"]
    with st.sidebar:
        st.markdown('<div class="hr-wordmark">HEDEGREEN RESEARCH<span class="dot"> ●</span></div>', unsafe_allow_html=True)
        st.markdown("**Norwegian Politics Data**")
        if os.environ.get("WPD_NORWAY_RELEASE_CANDIDATE") == "true":
            st.caption("Local release candidate · not published")
        elif os.environ.get("WPD_PUBLIC_PREVIEW") == "true":
            st.caption("Public Norway preview")
        st.markdown(
            "<p style='font-size:0.75rem;color:#6a6a7a;line-height:1.6;margin-top:0.3rem;'>"
            "Storting 2025: 357 current municipalities and six factors. Storting 2021: turnout only, across 355 municipalities; Ålesund and Haram are excluded."
            "</p>",
            unsafe_allow_html=True,
        )
        st.divider()
        party_name_mode = render_party_name_selector(country_config.party_metadata, key="norway_party_name_mode")
        st.divider()
        page = st.radio(
            "nav",
            ["Explore", "By Municipality", "National trends", "About & sources"],
            label_visibility="collapsed",
            key="norway_page",
        )
        st.divider()
        render_country_sidebar_footer(country_config)

    if page == "Explore":
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Norwegian Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("Is there a pattern?")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:2rem;'>"
            "Explore municipality-level patterns in the 2025 Storting election, or turnout patterns in the limited 2021 municipality layer."
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="step-label">Step 1 — Election year</div>', unsafe_allow_html=True)
        year = st.selectbox(
            "year",
            options=sorted(NORWAY_LIVE_YEARS, reverse=True),
            index=0,
            key="norway_year",
            label_visibility="collapsed",
        )
        municipal_year = municipal[municipal["election_year"] == year].copy()
        if year == 2021:
            st.info("2021 covers 355 current municipalities and turnout only. Ålesund and Haram are excluded because the old Ålesund result cannot be divided reliably between them. National 2021 results use the full country.")
        else:
            st.caption("2025 covers all 357 current municipalities. Factors use their 2025 measurements; income 2024 is held outside this analysis.")

        metric_items = available_norway_metric_items(year, factor_frames)
        metric_labels = [label for _, label, _ in metric_items]
        st.markdown('<div class="step-label" style="margin-top:1rem;">Step 2 — Pick factors</div>', unsafe_allow_html=True)
        selected_metric_labels = st.pills(
            "norway-factors",
            metric_labels,
            key=f"norway_cx_factors_{year}",
            selection_mode="multi",
            label_visibility="collapsed",
        )
        if selected_metric_labels:
            st.caption(" ".join(NORWAY_FACTOR_METHOD_NOTES[key] for key, label, _ in metric_items if label in selected_metric_labels))

        party_profiles = get_norway_party_profiles(municipal_year)
        all_party_options = party_profiles["party"].tolist()
        default_public_parties = party_profiles.loc[party_profiles["default_public"], "party"].tolist()
        party_options = default_public_parties
        default_parties = default_public_parties[:5]
        if "norway_parties" not in st.session_state:
            st.session_state["norway_parties"] = default_parties
        st.markdown('<div class="step-label" style="margin-top:1rem;">Step 3 — Pick parties</div>', unsafe_allow_html=True)
        include_low_coverage = st.checkbox(
            "Show smaller parties too",
            key="norway_include_low_coverage",
            help="Default Norway view keeps only parties with at least 25 municipalities and at least 0.5% mean municipality vote share. This avoids thin-coverage micro-party correlations dominating the results.",
        )
        party_options = all_party_options if include_low_coverage else default_public_parties
        current_selected = [party for party in st.session_state.get("norway_parties", []) if party in party_options]
        if not current_selected:
            current_selected = party_options[:] if st.session_state.get("norway_all_parties") else party_options[:1]
        st.session_state["norway_parties"] = current_selected
        select_all = st.checkbox("All parties", key="norway_all_parties")
        if select_all:
            selected_parties = party_options
            st.session_state["norway_parties"] = party_options
        else:
            selected_parties = st.pills(
                "norway-parties",
                party_options,
                key="norway_parties",
                selection_mode="multi",
                format_func=lambda party: format_party_name(party, metadata=country_config.party_metadata, mode=party_name_mode, compact=True),
                label_visibility="collapsed",
            )
        st.markdown(
            "<p style='font-size:0.72rem;color:#8888a0;margin-top:0.35rem;margin-bottom:0;'>"
            "Default party view filters out micro-parties and thin-coverage regional lists.</p>",
            unsafe_allow_html=True,
        )

        if not selected_metric_labels or not selected_parties:
            st.markdown(
                '<div class="finding weak">'
                '<div class="strength-tag">SELECTION INCOMPLETE</div>'
                '<div class="headline">This analysis cannot run yet.</div>'
                '<div class="body">Norway municipality-level correlation requires at least one factor and at least one party selection.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            return

        factor_label_to_key = {label: key for key, label, _ in metric_items}
        results = []
        for party in selected_parties:
            votes = municipal_year[municipal_year["party"] == party][["municipality", "share"]]
            for metric_label in selected_metric_labels:
                metric_key = factor_label_to_key[metric_label]
                metric_series = _get_metric_series(metric_key, year, factor_frames)
                merged = votes.merge(metric_series, on="municipality", how="inner")
                computed = compute_correlation_result(
                    merged,
                    factor=metric_label,
                    party=party,
                    year=year,
                    mode="explore-norway",
                )
                results.append(
                    {
                        "party": party,
                        "factor": metric_label,
                        "metric_key": metric_key,
                        "label": _metric_label(metric_key),
                        "r": computed["r"],
                        "merged": computed["merged"],
                        "valid": computed["valid"],
                        "strength": corr_strength_label(computed["r"]),
                    }
                )

        valid_results = [row for row in results if row["valid"]]
        if not valid_results:
            st.markdown(
                '<div class="finding weak">'
                '<div class="strength-tag">NO VALID RESULT</div>'
                '<div class="headline">No valid Norway result is available</div>'
                '<div class="body">The current selection did not produce a reliable municipality-level correlation value.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            return

        if len(selected_parties) == 1 and len(selected_metric_labels) == 1:
            row = valid_results[0]
            strength_cls, strength_tag, headline, concrete, copy_sentence, note = build_country_finding(
                row["r"],
                row["factor"],
                row["label"],
                row["party"],
                year,
                row["merged"],
                party_name_mode,
                country_config,
            )
            st.markdown(
                f"<div class='finding {strength_cls}'>"
                f"<div class='strength-tag'>{strength_tag}</div>"
                f"<div class='headline'>{headline}</div>"
                f"<div class='body'>{concrete}</div>"
                f"<div class='footnote'>{note}</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            ranked = row["merged"].sort_values("metric").rename(
                columns={"municipality": "Municipality", "metric": METRIC_SHORT_LABELS.get(row["factor"], row["label"]), "share": "Vote share"}
            )
            render_compact_dataframe(ranked.head(10))
        else:
            top = max(valid_results, key=lambda item: abs(float(item["r"])))
            st.markdown(
                f"<p style='font-size:0.75rem;color:#aaaabc;margin-bottom:0.5rem;'>Showing the strongest live {year} Norway signal first. See the full table below for the rest.</p>",
                unsafe_allow_html=True,
            )
            strength_cls, strength_tag, headline, concrete, _, note = build_country_finding(
                top["r"],
                top["factor"],
                top["label"],
                top["party"],
                year,
                top["merged"],
                party_name_mode,
                country_config,
            )
            st.markdown(
                f"<div class='finding {strength_cls}'>"
                f"<div class='strength-tag'>{strength_tag}</div>"
                f"<div class='headline'>{headline}</div>"
                f"<div class='body'>{concrete}</div>"
                f"<div class='footnote'>{note}</div>"
                "</div>",
                unsafe_allow_html=True,
            )
            flat_df = pd.DataFrame(
                [
                    {
                        "Party": format_party_name(row["party"], metadata=country_config.party_metadata, mode=party_name_mode),
                        "Factor": row["factor"],
                        "r": row["r"],
                        "Strength": row["strength"],
                    }
                    for row in valid_results
                ]
            ).assign(abs_r=lambda frame: frame["r"].abs()).sort_values("abs_r", ascending=False).drop(columns="abs_r")
            render_compact_dataframe(flat_df)

    elif page == "By Municipality":
        year = 2025
        municipal_2025 = municipal[municipal["election_year"] == year].copy()
        party_options = _party_options(municipal_2025, year)
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Norwegian Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("By Municipality")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:1.5rem;'>"
            "Current-safe municipality ranking for the 2025 Storting layer.</p>",
            unsafe_allow_html=True,
        )
        party = st.selectbox(
            "Party",
            party_options,
            format_func=lambda value: format_party_name(value, metadata=country_config.party_metadata, mode=party_name_mode),
            key="norway_single_party",
        )
        filtered = municipal_2025[municipal_2025["party"] == party].sort_values("share", ascending=False)
        render_compact_dataframe(
            filtered[["municipality", "share"]].rename(columns={"municipality": "Municipality", "share": "Vote %"})
        )

    elif page == "National trends":
        st.caption("Official national vote shares for the full country in 2021 and 2025. These totals are independent of the 355-municipality restriction in the 2021 turnout analysis.")
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Norwegian Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("National trends")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:1.5rem;'>"
            "First internal national Norway summary using the 2021 and 2025 Storting layers.</p>",
            unsafe_allow_html=True,
        )
        ordered = national[national["election_year"] == national["election_year"].max()].sort_values("share", ascending=False)["party"].tolist()
        selected = st.multiselect(
            "Parties",
            ordered,
            default=ordered[:5],
            format_func=lambda party: format_party_name(party, metadata=country_config.party_metadata, mode=party_name_mode, compact=True),
            key="norway_national_parties",
        )
        if selected:
            chart_df = national[national["party"].isin(selected)].copy()
            chart_df["party_label"] = chart_df["party"].apply(
                lambda party: format_party_name(party, metadata=country_config.party_metadata, mode=party_name_mode, compact=True)
            )
            render_national_trend_chart(chart_df, "election_year", "party_label", "share")
            pivot = chart_df.pivot_table(index="election_year", columns="party_label", values="share")
            st.dataframe(format_display_table(pivot, decimals=2), width="stretch")

    else:
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Norwegian Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("About & sources")
        st.markdown(
            f"""
Norwegian Politics Data compares Storting vote shares with municipality-level factors.

- Country: `{country_config.display_name}`
- Municipality scope: `2025` with all `357` current municipalities; `2021` turnout only with `355`
- National trend scope: full-country official vote shares for `2021` and `2025`
- Geography: `{country_config.public_geography_label}`
- Current municipality count: `{country_config.public_geography_count}`
- Statistics source: `{country_config.statistics_source_name}`

The 2025 factor picker includes population, population density, age 65+, turnout, cars and education. Income is available as 2024 context data and is not relabelled as a 2025 measurement.
"""
        )
        st.markdown(
            """
**Method note**
- Correlation is not causation.
- `2021` exists in the municipality correlation UI only as a bridge-safe turnout mode.
- `2021` bridge-safe municipality readings cover `355` current municipalities and exclude current `Ålesund` and `Haram`, because old `Ålesund` cannot be split honestly across the 2024 municipal reform from the available official municipality-level result.
- The incomplete Haram reconstruction is not used as a municipality result. Pooled advance votes prevent a defensible split of old Ålesund.
- The 2025 picker offers six factors, including direct 2025 education coverage for all 357 municipalities; for `2021`, only `turnout` is available.
- `Cars` uses the 2025 SSB private-car layer only; earlier vehicle years stay out because SSB changed the municipality placement rule for leased vehicles in 2025.
- Default party view filters out micro-parties and thin-coverage regional lists before `All parties` runs.
- Patterns describe municipalities, not individual voters. A result does not establish why a person voted for a party.
- Factor municipality names are aligned by current municipality code. Source spelling differences, such as Fauske's Sami name, do not remove a municipality from the analysis.
"""
        )
        factor_rows = []
        for key, label, _ in NORWAY_METRIC_OPTIONS:
            frame = factor_frames.get(key, pd.DataFrame())
            years = sorted(frame["year"].unique().tolist()) if not frame.empty else []
            visible_years = [year for year in NORWAY_LIVE_YEARS if any(item[0] == key for item in available_norway_metric_items(year, factor_frames))]
            factor_rows.append({"Factor": label, "Picker election years": ", ".join(map(str, visible_years)) or "—", "Data reference years": ", ".join(map(str, years)) or "—", "Measure": NORWAY_FACTOR_METHOD_NOTES[key]})
        factor_rows.append({"Factor": "Income", "Picker election years": "Not offered", "Data reference years": "2024", "Measure": "Median ordinary income after special deduction; residents aged 17+ (SSB 05671). Context only."})
        render_compact_dataframe(pd.DataFrame(factor_rows))
        st.subheader("Data sources")
        st.markdown(
            """
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/08092">Statistics Norway table 08092</a></strong> — Storting votes by party and municipality.</div>
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/08243">Statistics Norway table 08243</a></strong> — Storting turnout by municipality.</div>
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/11342">Statistics Norway table 11342</a></strong> — Population and population density.</div>
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/07459">Statistics Norway table 07459</a></strong> — Age 65+ share.</div>
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/07849">Statistics Norway table 07849</a></strong> — Private cars per 1,000 residents, 2025 only.</div>
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/05671">Statistics Norway table 05671</a></strong> — Income, held back from live picker for now.</div>
<div class="source-item"><strong><a href="https://www.ssb.no/en/statbank/table/09429">Statistics Norway table 09429</a></strong> — Short + long higher education, aged 16+, used for the 2025 election view.</div>
<div class="source-item"><strong>Municipality bridge</strong> — Direct code/name mappings for 2021 to current geography; unresolved Ålesund/Haram rows are excluded.</div>
            """,
            unsafe_allow_html=True,
        )
