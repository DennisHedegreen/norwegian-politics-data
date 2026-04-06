from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from core.correlation import compute_correlation_result, corr_strength_label
from core.presentation import (
    METRIC_SHORT_LABELS,
    PARTY_NAME_MODES,
    build_country_finding,
    format_display_table,
    format_party_name,
    render_bar_chart,
    render_compact_dataframe,
    render_country_sidebar_footer,
    render_national_trend_chart,
)


NORWAY_LIVE_FACTOR_KEYS = ("population", "density", "age65", "turnout", "cars")
NORWAY_LIVE_YEARS = (2025,)
NORWAY_DEFAULT_PARTY_MIN_MUNICIPALITIES = 25
NORWAY_DEFAULT_PARTY_MIN_MEAN_SHARE = 0.5
NORWAY_METRIC_OPTIONS = [
    ("population", "Population", "Population (reference count)"),
    ("density", "Population density", "Residents per km²"),
    ("age65", "Age 65+", "Share aged 65+ (%)"),
    ("turnout", "Turnout", "Votes cast as share of voters (%)"),
    ("cars", "Cars", "Passenger cars per 1,000 residents"),
]


def _factor_file(country_config, filename: str) -> Path:
    return country_config.factor_dir / filename


def is_available(country_config, runtime_context) -> bool:
    return country_config.municipal_vote_path.exists() and country_config.factor_dir.exists()


@st.cache_data
def load_bundle(country_config):
    municipal = pd.read_csv(country_config.municipal_vote_path)
    municipal["election_year"] = municipal["election_year"].astype(int)
    municipal["share"] = municipal["share"].astype(float)

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
            filename = "turnout_pct.csv"
        elif metric_key == "income":
            filename = "income.csv"
        elif metric_key == "education":
            filename = "education.csv"
        elif metric_key == "cars":
            filename = "cars_per_1000.csv"
        if filename is None:
            continue
        path = _factor_file(country_config, filename)
        frame = pd.read_csv(path) if path.exists() else pd.DataFrame(columns=["municipality", "year", "value"])
        if not frame.empty and "year" in frame.columns:
            frame["year"] = frame["year"].astype(int)
        factor_frames[metric_key] = frame

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
    municipalities = sorted(municipal.loc[municipal["election_year"] == 2025, "municipality"].dropna().unique().tolist())

    with st.sidebar:
        st.markdown('<div class="hr-wordmark">HEDEGREEN RESEARCH<span class="dot"> ●</span></div>', unsafe_allow_html=True)
        st.markdown("**Norwegian Politics Data**")
        st.markdown(
            "<p style='font-size:0.75rem;color:#6a6a7a;line-height:1.6;margin-top:0.3rem;'>"
            "Internal Norway adapter. Normal municipality reading is currently locked to the clean 2025 current-municipality layer."
            "</p>",
            unsafe_allow_html=True,
        )
        st.divider()
        party_name_mode = st.selectbox("Party names", PARTY_NAME_MODES, index=1, key="norway_party_name_mode")
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
        year = NORWAY_LIVE_YEARS[0]
        municipal_2025 = municipal[municipal["election_year"] == year].copy()
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Norwegian Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("Is there a pattern?")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:2rem;'>"
            "First internal Norway reading. Municipality correlations currently use only the honest 2025 current-municipality layer."
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="step-label">Step 1 — Election year</div>', unsafe_allow_html=True)
        st.selectbox(
            "year",
            options=[year],
            index=0,
            key="norway_year",
            label_visibility="collapsed",
            disabled=True,
        )

        metric_items = [(key, label, metric_label) for key, label, metric_label in NORWAY_METRIC_OPTIONS if not _get_metric_series(key, year, factor_frames).empty]
        metric_labels = [label for _, label, _ in metric_items]
        st.markdown('<div class="step-label" style="margin-top:1rem;">Step 2 — Pick factors</div>', unsafe_allow_html=True)
        selected_metric_labels = st.pills(
            "norway-factors",
            metric_labels,
            key="norway_cx_factors",
            selection_mode="multi",
            label_visibility="collapsed",
        )

        party_profiles = get_norway_party_profiles(municipal_2025)
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
            votes = municipal_2025[municipal_2025["party"] == party][["municipality", "share"]]
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
                "<p style='font-size:0.75rem;color:#aaaabc;margin-bottom:0.5rem;'>Showing the strongest live 2025 Norway signal first. See the full table below for the rest.</p>",
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
This is the first internal Norway adapter inside `World-politics-data`.

- Country: `{country_config.display_name}`
- Election scope in normal UI: `2025 Storting municipality-safe current layer`
- Internal national trend scope: `2021`, `2025`
- Public geography: `{country_config.public_geography_label}`
- Public geography count: `{country_config.public_geography_count}`
- Statistics source: `{country_config.statistics_source_name}`

The Norway data pack already contains `income` and `education`, but the live Norway factor picker intentionally hides them for now because the first honest municipality correlation window is narrower than the full harvest.
"""
        )
        st.markdown(
            """
**Method note**
- Correlation is not causation.
- `2021` exists in the harvest, but it stays outside the normal municipality correlation UI in this first adapter pass.
- `Haram 2021 partial` remains internal-only and never appears as a normal municipality row.
- The first normal Norway factor picker is intentionally restricted to `population`, `population density`, `age65`, `turnout`, and `cars`.
- `Cars` uses the 2025 SSB private-car layer only; earlier vehicle years stay out because SSB changed the municipality placement rule for leased vehicles in 2025.
- Default party view filters out micro-parties and thin-coverage regional lists before `All parties` runs.
"""
        )
        factor_rows = []
        for key, label, _ in NORWAY_METRIC_OPTIONS:
            frame = factor_frames.get(key, pd.DataFrame())
            years = sorted(frame["year"].unique().tolist()) if not frame.empty else []
            factor_rows.append({"Factor": label, "Visible in live picker": "Yes", "Years": ", ".join(str(year) for year in years) or "—"})
        factor_rows.extend(
            [
                {"Factor": "Income", "Visible in live picker": "No", "Years": "2024"},
                {"Factor": "Education", "Visible in live picker": "No", "Years": "2024"},
            ]
        )
        render_compact_dataframe(pd.DataFrame(factor_rows))
        st.subheader("Data sources")
        st.markdown(
            """
<div class="source-item"><strong>Statistics Norway table 08092</strong> — Storting votes by party and municipality.</div>
<div class="source-item"><strong>Statistics Norway table 08243</strong> — Storting turnout by municipality.</div>
<div class="source-item"><strong>Statistics Norway table 11342</strong> — Population and population density.</div>
<div class="source-item"><strong>Statistics Norway table 07459</strong> — Age 65+ share.</div>
<div class="source-item"><strong>Statistics Norway table 07849</strong> — Private cars per 1,000 residents, 2025 only.</div>
<div class="source-item"><strong>Statistics Norway table 05671</strong> — Income, held back from live picker for now.</div>
<div class="source-item"><strong>Statistics Norway table 09429</strong> — Education, held back from live picker for now.</div>
<div class="source-item"><strong>Valgdirektoratet API</strong> — Internal-only Haram 2021 partial rule notes.</div>
            """,
            unsafe_allow_html=True,
        )
