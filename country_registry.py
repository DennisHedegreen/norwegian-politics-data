from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent


BASE_FACTOR_CATALOG = {'population': {'label': 'Population',
                'metric_label': 'Population (reference count)',
                'question': 'Do larger municipalities vote differently?',
                'filename': 'population.csv',
                'comparability_status': 'country_local'},
 'density': {'label': 'Population density',
             'metric_label': 'Residents per km²',
             'question': 'Does dense settlement correlate with voting '
                         'behaviour?',
             'filename': 'population_density.csv',
             'comparability_status': 'country_local'},
 'age65': {'label': 'Age 65+',
           'metric_label': 'Share aged 65+ (%)',
           'question': 'Do older municipalities vote differently?',
           'filename': 'age65_pct.csv',
           'comparability_status': 'family_mapped'},
 'turnout': {'label': 'Turnout',
             'metric_label': 'Votes cast as share of voters (%)',
             'question': 'Do high-turnout municipalities vote differently?',
             'filename': 'turnout_pct.csv',
             'comparability_status': 'family_mapped'},
 'cars': {'label': 'Cars',
          'metric_label': 'Passenger cars per 1,000 residents',
          'question': 'Do car-heavy (rural) areas vote differently from urban '
                      'ones?',
          'filename': 'cars_per_1000.csv',
          'comparability_status': 'country_local'},
 'income': {'label': 'Income',
            'metric_label': 'Avg. disposable income',
            'question': 'Do wealthier municipalities vote differently?',
            'filename': 'income.csv',
            'comparability_status': 'family_mapped'},
 'education': {'label': 'Education',
               'metric_label': 'Higher education share (%)',
               'question': 'Do more educated municipalities vote differently?',
               'filename': 'education.csv',
               'comparability_status': 'family_mapped'}}

PARTY_METADATA = {'Labour Party': {'native': 'Arbeiderpartiet',
                  'english': 'Labour Party',
                  'short_native': 'Arbeiderpartiet',
                  'short_english': 'Labour Party',
                  'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                  'verified_on': '2026-10-15',
                  'translation_status': 'documented_english',
                  'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                  'source_party_id': '01'},
 'Progress Party': {'native': 'Fremskrittspartiet',
                    'english': 'Progress Party',
                    'short_native': 'Fremskrittspartiet',
                    'short_english': 'Progress Party',
                    'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                    'verified_on': '2026-10-15',
                    'translation_status': 'documented_english',
                    'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                    'source_party_id': '02'},
 'Conservative Party': {'native': 'Høyre',
                        'english': 'Conservative Party',
                        'short_native': 'Høyre',
                        'short_english': 'Conservative Party',
                        'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                        'verified_on': '2026-10-15',
                        'translation_status': 'documented_english',
                        'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                        'source_party_id': '03'},
 'Christian Democratic Party': {'native': 'Kristelig Folkeparti',
                                'english': 'Christian Democratic Party',
                                'short_native': 'Kristelig Folkeparti',
                                'short_english': 'Christian Democratic Party',
                                'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                'verified_on': '2026-10-15',
                                'translation_status': 'documented_english',
                                'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                'source_party_id': '04'},
 'Centre Party': {'native': 'Senterpartiet',
                  'english': 'Centre Party',
                  'short_native': 'Senterpartiet',
                  'short_english': 'Centre Party',
                  'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                  'verified_on': '2026-10-15',
                  'translation_status': 'documented_english',
                  'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                  'source_party_id': '05'},
 'Socialist Left Party': {'native': 'Sosialistisk Venstreparti',
                          'english': 'Socialist Left Party',
                          'short_native': 'Sosialistisk Venstreparti',
                          'short_english': 'Socialist Left Party',
                          'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                          'verified_on': '2026-10-15',
                          'translation_status': 'documented_english',
                          'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                          'source_party_id': '06'},
 'Liberal Party': {'native': 'Venstre',
                   'english': 'Liberal Party',
                   'short_native': 'Venstre',
                   'short_english': 'Liberal Party',
                   'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                   'verified_on': '2026-10-15',
                   'translation_status': 'documented_english',
                   'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                   'source_party_id': '07'},
 'Green Party': {'native': 'Miljøpartiet de Grønne',
                 'english': 'Green Party',
                 'short_native': 'Miljøpartiet de Grønne',
                 'short_english': 'Green Party',
                 'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                 'verified_on': '2026-10-15',
                 'translation_status': 'documented_english',
                 'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                 'source_party_id': '08'},
 'Communist Party of Norway': {'native': 'Norges Kommunistiske Parti',
                               'english': 'Communist Party of Norway',
                               'short_native': 'Norges Kommunistiske Parti',
                               'short_english': 'Communist Party of Norway',
                               'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                               'verified_on': '2026-10-15',
                               'translation_status': 'documented_english',
                               'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                               'source_party_id': '09'},
 "The Pensioners' Party": {'native': 'Pensjonistpartiet',
                           'english': "The Pensioners' Party",
                           'short_native': 'Pensjonistpartiet',
                           'short_english': "The Pensioners' Party",
                           'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                           'verified_on': '2026-10-15',
                           'translation_status': 'documented_english',
                           'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                           'source_party_id': '10'},
 'Democratic Party of Norway': {'native': 'Demokratene i Norge',
                                'english': 'Democratic Party of Norway',
                                'short_native': 'Demokratene i Norge',
                                'short_english': 'Democratic Party of Norway',
                                'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                'verified_on': '2026-10-15',
                                'translation_status': 'documented_english',
                                'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                'source_party_id': '122'},
 'Conservative': {'native': 'Konservativt',
                  'english': 'Conservative',
                  'short_native': 'Konservativt',
                  'short_english': 'Conservative',
                  'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                  'verified_on': '2026-10-15',
                  'translation_status': 'documented_english',
                  'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                  'source_party_id': '123'},
 'Piratpartiet': {'native': 'Piratpartiet',
                  'english': 'Piratpartiet',
                  'short_native': 'Piratpartiet',
                  'short_english': 'Piratpartiet',
                  'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                  'verified_on': '2026-10-15',
                  'translation_status': 'source_label',
                  'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                  'source_party_id': '124'},
 'Feministisk Initiativ': {'native': 'Feministisk Initiativ',
                           'english': 'Feministisk Initiativ',
                           'short_native': 'Feministisk Initiativ',
                           'short_english': 'Feministisk Initiativ',
                           'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                           'verified_on': '2026-10-15',
                           'translation_status': 'source_label',
                           'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                           'source_party_id': '131'},
 'The Welfare and Innovation Party': {'native': 'Velferd og innovasjonspartiet',
                                      'english': 'The Welfare and Innovation '
                                                 'Party',
                                      'short_native': 'Velferd og '
                                                      'innovasjonspartiet',
                                      'short_english': 'The Welfare and '
                                                       'Innovation Party',
                                      'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                      'verified_on': '2026-10-15',
                                      'translation_status': 'documented_english',
                                      'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                      'source_party_id': '132'},
 'Capitalist Party of Norway': {'native': 'Liberalistene',
                                'english': 'Capitalist Party of Norway',
                                'short_native': 'Liberalistene',
                                'short_english': 'Capitalist Party of Norway',
                                'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                'verified_on': '2026-10-15',
                                'translation_status': 'documented_english',
                                'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                'source_party_id': '133'},
 'Alliansen - Alternative for Norway': {'native': 'Alliansen - Alternativ for '
                                                  'Norge',
                                        'english': 'Alliansen - Alternative '
                                                   'for Norway',
                                        'short_native': 'Alliansen - '
                                                        'Alternativ for Norge',
                                        'short_english': 'Alliansen - '
                                                         'Alternative for '
                                                         'Norway',
                                        'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                        'verified_on': '2026-10-15',
                                        'translation_status': 'documented_english',
                                        'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                        'source_party_id': '150'},
 'Folkeaksjonen Nei til mer bompenger': {'native': 'Folkeaksjonen Nei til mer '
                                                   'bompenger',
                                         'english': 'Folkeaksjonen Nei til mer '
                                                    'bompenger',
                                         'short_native': 'Folkeaksjonen Nei '
                                                         'til mer bompenger',
                                         'short_english': 'Folkeaksjonen Nei '
                                                          'til mer bompenger',
                                         'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                         'verified_on': '2026-10-15',
                                         'translation_status': 'source_label',
                                         'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                         'source_party_id': '151',
                                         'name_note': 'Preserved election-era '
                                                      'label; current metadata '
                                                      'uses Folkets parti. No '
                                                      'historical rename.'},
 'Industrial-, commerce & business Party': {'native': 'Industri- og '
                                                      'Næringspartiet',
                                            'english': 'Industrial-, commerce '
                                                       '& business Party',
                                            'short_native': 'Industri- og '
                                                            'Næringspartiet',
                                            'short_english': 'Industrial-, '
                                                             'commerce & '
                                                             'business Party',
                                            'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                                            'verified_on': '2026-10-15',
                                            'translation_status': 'documented_english',
                                            'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                                            'source_party_id': '152'},
 'Partiet Sentrum': {'native': 'Partiet Sentrum',
                     'english': 'Partiet Sentrum',
                     'short_native': 'Partiet Sentrum',
                     'short_english': 'Partiet Sentrum',
                     'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                     'verified_on': '2026-10-15',
                     'translation_status': 'source_label',
                     'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                     'source_party_id': '153'},
 'Generation Party': {'native': 'Generasjonspartiet',
                      'english': 'Generation Party',
                      'short_native': 'Generasjonspartiet',
                      'short_english': 'Generation Party',
                      'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                      'verified_on': '2026-10-15',
                      'translation_status': 'documented_english',
                      'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                      'source_party_id': '154'},
 'Pasientfokus': {'native': 'Pasientfokus',
                  'english': 'Pasientfokus',
                  'short_native': 'Pasientfokus',
                  'short_english': 'Pasientfokus',
                  'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                  'verified_on': '2026-10-15',
                  'translation_status': 'source_label',
                  'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                  'source_party_id': '155'},
 'Redd Naturen': {'native': 'Redd Naturen',
                  'english': 'Redd Naturen',
                  'short_native': 'Redd Naturen',
                  'short_english': 'Redd Naturen',
                  'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                  'verified_on': '2026-10-15',
                  'translation_status': 'source_label',
                  'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                  'source_party_id': '156'},
 'The Loneliness Party': {'native': 'Ensomhetspartiet',
                          'english': 'The Loneliness Party',
                          'short_native': 'Ensomhetspartiet',
                          'short_english': 'The Loneliness Party',
                          'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                          'verified_on': '2026-10-15',
                          'translation_status': 'documented_english',
                          'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                          'source_party_id': '157'},
 'Peace and Justice': {'native': 'Fred og Rettferdighet (FOR)',
                       'english': 'Peace and Justice',
                       'short_native': 'Fred og Rettferdighet (FOR)',
                       'short_english': 'Peace and Justice',
                       'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                       'verified_on': '2026-10-15',
                       'translation_status': 'documented_english',
                       'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                       'source_party_id': '158'},
 'The DNI Party': {'native': 'Partiet DNI',
                   'english': 'The DNI Party',
                   'short_native': 'Partiet DNI',
                   'short_english': 'The DNI Party',
                   'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                   'verified_on': '2026-10-15',
                   'translation_status': 'documented_english',
                   'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                   'source_party_id': '159'},
 'Save Ullev�l Hospital': {'native': 'Redd Ullevål sykehus',
                           'english': 'Save Ullevål Hospital',
                           'short_native': 'Redd Ullevål sykehus',
                           'short_english': 'Save Ullevål Hospital',
                           'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                           'verified_on': '2026-10-15',
                           'translation_status': 'documented_english',
                           'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                           'source_party_id': '160'},
 'Coastal Party': {'native': 'Kystpartiet',
                   'english': 'Coastal Party',
                   'short_native': 'Kystpartiet',
                   'short_english': 'Coastal Party',
                   'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
                   'verified_on': '2026-10-15',
                   'translation_status': 'documented_english',
                   'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
                   'source_party_id': '44'},
 'Red Party': {'native': 'Rødt',
               'english': 'Red Party',
               'short_native': 'Rødt',
               'short_english': 'Red Party',
               'source_url': 'https://data.ssb.no/api/v0/en/table/08092',
               'verified_on': '2026-10-15',
               'translation_status': 'documented_english',
               'native_source_url': 'https://data.ssb.no/api/v0/no/table/08092',
               'source_party_id': '55'}}


@dataclass(frozen=True)
class CountryConfig:
    country_id: str
    display_name: str
    adjective: str
    language: str
    statistics_source_name: str
    default_election_type: str
    election_label: str
    public_geography_type: str
    public_geography_label: str
    public_geography_label_plural: str
    public_geography_count: int
    supported_factors: tuple[str, ...]
    supported_elections: tuple[str, ...]
    internal_ready: bool
    public_ready: bool
    municipal_vote_path: Path
    national_vote_path: Path | None
    factor_dir: Path
    party_metadata: dict[str, dict[str, str]]
    source_note: str
    secondary_source_note: str | None = None

    def factor_catalog(self) -> list[dict[str, str]]:
        return [{**BASE_FACTOR_CATALOG[key], "key": key} for key in self.supported_factors]


COUNTRY = CountryConfig(
    country_id='norway',
    display_name='Norway',
    adjective='Norwegian',
    language='English',
    statistics_source_name='Statistics Norway',
    default_election_type='storting',
    election_label='Storting election',
    public_geography_type='municipality',
    public_geography_label='municipality',
    public_geography_label_plural='municipalities',
    public_geography_count=357,
    supported_factors=('population', 'density', 'age65', 'turnout', 'cars', 'income', 'education'),
    supported_elections=('storting',),
    internal_ready=True,
    public_ready=True,
    municipal_vote_path=ROOT / "norway/storting/storting_party_share_by_current_municipality_bridge_safe.csv",
    national_vote_path=ROOT / "norway/storting/storting_national_vote_share.csv",
    factor_dir=ROOT / "norway/factors",
    party_metadata=PARTY_METADATA,
    source_note='Statistics Norway Storting municipality bridge-safe layer + factor harvests',
    secondary_source_note='Valgdirektoratet partial territorial notes stay internal-only',
)


def get_country_config(country_id: str) -> CountryConfig:
    if country_id != COUNTRY.country_id:
        raise KeyError(f"Unknown country_id: {country_id}")
    return COUNTRY


def list_public_countries() -> list[CountryConfig]:
    return [COUNTRY] if COUNTRY.public_ready else []


def list_internal_countries() -> list[CountryConfig]:
    return [COUNTRY] if COUNTRY.internal_ready else []


def country_data_pack_exists(config: CountryConfig) -> bool:
    if not config.municipal_vote_path.exists():
        return False
    if not config.factor_dir.exists():
        return False
    return True


def _normalize_allowed_country_ids(allowed_country_ids: Iterable[str] | None) -> list[str] | None:
    if allowed_country_ids is None:
        return None
    return [country_id.strip().lower() for country_id in allowed_country_ids if country_id.strip()]


def list_exposed_countries(
    allowed_country_ids: Iterable[str] | None = None,
    *,
    allow_internal: bool = False,
    require_data_pack: bool = True,
) -> list[CountryConfig]:
    allowed = _normalize_allowed_country_ids(allowed_country_ids)
    if allow_internal:
        if not COUNTRY.internal_ready:
            return []
    elif not COUNTRY.public_ready:
        return []
    if allowed is None:
        if require_data_pack and not country_data_pack_exists(COUNTRY):
            return []
        return [COUNTRY]
    if COUNTRY.country_id not in allowed:
        return []
    if require_data_pack and not country_data_pack_exists(COUNTRY):
        return []
    return [COUNTRY]


def list_exposed_public_countries(
    allowed_country_ids: Iterable[str] | None = None,
    require_data_pack: bool = True,
) -> list[CountryConfig]:
    return list_exposed_countries(
        allowed_country_ids,
        allow_internal=False,
        require_data_pack=require_data_pack,
    )
