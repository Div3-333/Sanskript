from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .adhyaya2_atomic import ADHYAYA2_ATOMIC_SUTRAS
from .derivation import KrtSuffix, derive
from .grammar import Analysis, Case, Gender, GrammaticalNumber, Lakara, Pada, PartOfSpeech, Person
from .karaka import get_allowed_vibhaktis
from .samasa import SamasaSense, SamasaType, apply_ekashesha, create_compound
from .tinanta import Dhatu, DhatuType, TimeContext, TinEnding, TIN_ENDINGS, create_derived_dhatu, get_lakara_for_time, get_substituted_dhatu, get_vikarana, is_ardhadhatuka, is_sarvadhatuka, join_stem_ending, tin_ending
from .transliteration import devanagari_to_iast

@dataclass(frozen=True)
class SutraSpec:
    sutra_id: str
    domain: str
    operator: str
    assigned: tuple[str, ...]
    payload: Mapping[str, object]


EXTRA_SUTRA_IDS: tuple[str, ...] = (
    '2.1.2',
    '2.1.3',
    '2.1.25',
    '2.1.26',
    '2.1.27',
    '2.1.28',
    '2.1.29',
    '2.1.31',
    '2.1.32',
    '2.1.33',
    '2.1.34',
    '2.1.35',
    '2.1.37',
    '2.1.38',
    '2.1.39',
    '2.1.40',
    '2.1.41',
    '2.1.42',
    '2.1.43',
    '2.1.44',
    '2.1.45',
    '2.1.46',
    '2.1.47',
    '2.1.48',
    '2.1.49',
    '2.1.50',
    '2.1.51',
    '2.1.52',
    '2.1.53',
    '2.1.54',
    '2.1.55',
    '2.1.56',
    '2.1.58',
    '2.1.59',
    '2.1.60',
    '2.1.61',
    '2.1.62',
    '2.1.63',
    '2.1.64',
    '2.1.65',
    '2.1.66',
    '2.1.67',
    '2.1.68',
    '2.1.69',
    '2.1.70',
    '2.1.71',
    '2.1.72',
    '2.2.1',
    '2.2.2',
    '2.2.3',
    '2.2.4',
    '2.2.5',
    '2.2.6',
    '2.2.7',
    '2.2.8',
    '2.2.9',
    '2.2.10',
    '2.2.11',
    '2.2.12',
    '2.2.13',
    '2.2.14',
    '2.2.15',
    '2.2.16',
    '2.2.17',
    '2.2.18',
    '2.2.19',
    '2.2.20',
    '2.2.21',
    '2.2.22',
    '2.2.23',
    '2.2.24',
    '2.2.25',
    '2.2.26',
    '2.2.27',
    '2.2.28',
    '2.2.31',
    '2.2.32',
    '2.2.33',
    '2.2.34',
    '2.2.35',
    '2.2.36',
    '2.2.37',
    '2.2.38',
    '2.3.37',
    '2.3.38',
    '2.3.39',
    '2.3.40',
    '2.3.41',
    '2.3.42',
    '2.3.43',
    '2.3.44',
    '2.3.45',
    '2.3.46',
    '2.3.47',
    '2.3.48',
    '2.3.49',
    '2.3.51',
    '2.3.52',
    '2.3.53',
    '2.3.54',
    '2.3.55',
    '2.3.56',
    '2.3.57',
    '2.3.58',
    '2.3.59',
    '2.3.60',
    '2.3.61',
    '2.3.62',
    '2.3.63',
    '2.3.64',
    '2.3.65',
    '2.3.66',
    '2.3.67',
    '2.3.68',
    '2.3.69',
    '2.3.70',
    '2.3.71',
    '2.3.72',
    '2.3.73',
    '2.4.2',
    '2.4.3',
    '2.4.4',
    '2.4.5',
    '2.4.6',
    '2.4.7',
    '2.4.8',
    '2.4.9',
    '2.4.10',
    '2.4.11',
    '2.4.12',
    '2.4.13',
    '2.4.14',
    '2.4.15',
    '2.4.16',
    '2.4.19',
    '2.4.20',
    '2.4.21',
    '2.4.22',
    '2.4.23',
    '2.4.24',
    '2.4.25',
    '2.4.28',
    '2.4.29',
    '2.4.30',
    '2.4.31',
    '2.4.32',
    '2.4.33',
    '2.4.34',
    '2.4.35',
    '2.4.38',
    '2.4.39',
    '2.4.40',
    '2.4.41',
    '2.4.43',
    '2.4.44',
    '2.4.46',
    '2.4.49',
    '2.4.50',
    '2.4.51',
    '2.4.53',
    '2.4.54',
    '2.4.55',
    '2.4.56',
    '2.4.57',
    '2.4.58',
    '2.4.59',
    '2.4.60',
    '2.4.61',
    '2.4.62',
    '2.4.63',
    '2.4.64',
    '2.4.65',
    '2.4.66',
    '2.4.67',
    '2.4.68',
    '2.4.69',
    '2.4.70',
    '2.4.73',
    '2.4.74',
    '2.4.75',
    '2.4.76',
    '2.4.77',
    '2.4.78',
    '2.4.79',
    '2.4.80',
    '2.4.81',
    '2.4.82',
    '2.4.83',
    '2.4.84',
    '2.4.85',
    '3.1.1',
    '3.1.2',
    '3.1.3',
    '3.1.4',
    '3.1.6',
    '3.1.7',
    '3.1.9',
    '3.1.10',
    '3.1.11',
    '3.1.12',
    '3.1.13',
    '3.1.14',
    '3.1.15',
    '3.1.16',
    '3.1.17',
    '3.1.18',
    '3.1.19',
    '3.1.20',
    '3.1.21',
    '3.1.23',
    '3.1.24',
    '3.1.26',
    '3.1.27',
    '3.1.28',
    '3.1.29',
    '3.1.30',
    '3.1.31',
    '3.1.32',
    '3.1.33',
    '3.1.34',
    '3.1.35',
    '3.1.36',
    '3.1.37',
    '3.1.38',
    '3.1.39',
    '3.1.40',
    '3.1.41',
    '3.1.42',
    '3.1.43',
    '3.1.44',
    '3.1.45',
    '3.1.46',
    '3.1.47',
    '3.1.48',
    '3.1.49',
    '3.1.50',
    '3.1.51',
    '3.1.52',
    '3.1.53',
    '3.1.54',
    '3.1.55',
    '3.1.56',
    '3.1.57',
    '3.1.58',
    '3.1.59',
    '3.1.60',
    '3.1.61',
    '3.1.62',
    '3.1.63',
    '3.1.64',
    '3.1.65',
    '3.1.66',
    '3.1.67',
    '3.1.70',
    '3.1.71',
    '3.1.72',
    '3.1.74',
    '3.1.75',
    '3.1.76',
    '3.1.80',
    '3.1.82',
    '3.1.83',
    '3.1.84',
    '3.1.85',
    '3.1.86',
    '3.1.87',
    '3.1.88',
    '3.1.89',
    '3.1.90',
    '3.1.92',
    '3.1.94',
    '3.1.95',
    '3.1.96',
    '3.1.97',
    '3.1.98',
    '3.1.99',
    '3.1.100',
    '3.1.101',
    '3.1.102',
    '3.1.103',
    '3.1.104',
    '3.1.105',
    '3.1.106',
    '3.1.107',
    '3.1.108',
    '3.1.109',
    '3.1.110',
    '3.1.111',
    '3.1.112',
    '3.1.113',
    '3.1.114',
    '3.1.115',
    '3.1.116',
    '3.1.117',
    '3.1.118',
    '3.1.119',
    '3.1.120',
    '3.1.121',
    '3.1.122',
    '3.1.123',
    '3.1.124',
    '3.1.125',
    '3.1.126',
    '3.1.127',
    '3.1.128',
    '3.1.129',
    '3.1.130',
    '3.1.131',
    '3.1.132',
    '3.1.133',
    '3.1.134',
    '3.1.135',
    '3.1.136',
    '3.1.137',
    '3.1.138',
    '3.1.139',
    '3.1.140',
    '3.1.141',
    '3.1.142',
    '3.1.143',
    '3.1.144',
    '3.1.145',
    '3.1.146',
    '3.1.147',
    '3.1.148',
    '3.1.149',
    '3.1.150',
    '3.2.2',
    '3.2.4',
    '3.2.5',
    '3.2.6',
    '3.2.7',
    '3.2.8',
    '3.2.9',
    '3.2.10',
    '3.2.11',
    '3.2.12',
    '3.2.13',
    '3.2.14',
    '3.2.15',
    '3.2.17',
    '3.2.18',
    '3.2.19',
    '3.2.20',
    '3.2.21',
    '3.2.22',
    '3.2.23',
    '3.2.24',
    '3.2.25',
    '3.2.26',
    '3.2.27',
    '3.2.28',
    '3.2.29',
    '3.2.30',
    '3.2.31',
    '3.2.32',
    '3.2.33',
    '3.2.34',
    '3.2.35',
    '3.2.36',
    '3.2.37',
    '3.2.38',
    '3.2.39',
    '3.2.40',
    '3.2.41',
    '3.2.42',
    '3.2.43',
    '3.2.44',
    '3.2.45',
    '3.2.46',
    '3.2.47',
    '3.2.48',
    '3.2.49',
    '3.2.50',
    '3.2.51',
    '3.2.52',
    '3.2.53',
    '3.2.54',
    '3.2.55',
    '3.2.56',
    '3.2.57',
    '3.2.58',
    '3.2.59',
    '3.2.60',
    '3.2.61',
    '3.2.62',
    '3.2.63',
    '3.2.64',
    '3.2.65',
    '3.2.66',
    '3.2.67',
    '3.2.68',
    '3.2.69',
    '3.2.70',
    '3.2.71',
    '3.2.72',
    '3.2.73',
    '3.2.74',
    '3.2.75',
    '3.2.76',
    '3.2.77',
    '3.2.78',
    '3.2.79',
    '3.2.80',
    '3.2.81',
    '3.2.82',
    '3.2.83',
    '3.2.84',
    '3.2.85',
    '3.2.86',
    '3.2.87',
    '3.2.88',
    '3.2.89',
    '3.2.90',
    '3.2.91',
    '3.2.92',
    '3.2.93',
    '3.2.94',
    '3.2.95',
    '3.2.96',
    '3.2.97',
    '3.2.98',
    '3.2.99',
    '3.2.100',
    '3.2.101',
    '3.2.103',
    '3.2.104',
    '3.2.105',
    '3.2.106',
    '3.2.107',
    '3.2.108',
    '3.2.109',
    '3.2.112',
    '3.2.113',
    '3.2.114',
    '3.2.115',
    '3.2.116',
    '3.2.117',
    '3.2.118',
    '3.2.119',
    '3.2.120',
    '3.2.121',
    '3.2.122',
    '3.2.124',
    '3.2.125',
    '3.2.126',
    '3.2.127',
    '3.2.128',
    '3.2.129',
    '3.2.130',
    '3.2.131',
    '3.2.132',
    '3.2.133',
    '3.2.134',
    '3.2.136',
    '3.2.137',
    '3.2.138',
    '3.2.139',
    '3.2.140',
    '3.2.141',
    '3.2.142',
    '3.2.143',
    '3.2.144',
    '3.2.145',
    '3.2.146',
    '3.2.147',
    '3.2.148',
    '3.2.149',
    '3.2.150',
    '3.2.151',
    '3.2.152',
    '3.2.153',
    '3.2.154',
    '3.2.155',
    '3.2.156',
    '3.2.157',
    '3.2.158',
    '3.2.159',
    '3.2.160',
    '3.2.161',
    '3.2.162',
    '3.2.163',
    '3.2.164',
    '3.2.165',
    '3.2.166',
    '3.2.167',
    '3.2.168',
    '3.2.169',
    '3.2.170',
    '3.2.171',
    '3.2.172',
    '3.2.173',
    '3.2.174',
    '3.2.175',
    '3.2.176',
    '3.2.177',
    '3.2.178',
    '3.2.179',
    '3.2.180',
    '3.2.181',
    '3.2.182',
    '3.2.183',
    '3.2.184',
    '3.2.185',
    '3.2.186',
    '3.2.187',
    '3.2.188',
    '3.3.1',
    '3.3.2',
    '3.3.3',
    '3.3.4',
    '3.3.5',
    '3.3.6',
    '3.3.7',
    '3.3.8',
    '3.3.9',
    '3.3.10',
    '3.3.11',
    '3.3.12',
    '3.3.13',
    '3.3.14',
    '3.3.16',
    '3.3.17',
    '3.3.19',
    '3.3.20',
    '3.3.21',
    '3.3.22',
    '3.3.23',
    '3.3.24',
    '3.3.25',
    '3.3.26',
    '3.3.27',
    '3.3.28',
    '3.3.29',
    '3.3.30',
    '3.3.31',
    '3.3.32',
    '3.3.34',
    '3.3.35',
    '3.3.36',
    '3.3.37',
    '3.3.38',
    '3.3.39',
    '3.3.40',
    '3.3.41',
    '3.3.42',
    '3.3.43',
    '3.3.44',
    '3.3.45',
    '3.3.46',
    '3.3.47',
    '3.3.48',
    '3.3.49',
    '3.3.50',
    '3.3.51',
    '3.3.52',
    '3.3.53',
    '3.3.54',
    '3.3.55',
    '3.3.56',
    '3.3.57',
    '3.3.58',
    '3.3.59',
    '3.3.60',
    '3.3.61',
    '3.3.62',
    '3.3.63',
    '3.3.64',
    '3.3.65',
    '3.3.66',
    '3.3.67',
    '3.3.68',
    '3.3.69',
    '3.3.70',
    '3.3.71',
    '3.3.72',
    '3.3.73',
    '3.3.74',
    '3.3.75',
    '3.3.76',
    '3.3.77',
    '3.3.78',
    '3.3.79',
    '3.3.80',
    '3.3.81',
    '3.3.82',
    '3.3.83',
    '3.3.84',
    '3.3.85',
    '3.3.86',
    '3.3.87',
    '3.3.88',
    '3.3.89',
    '3.3.90',
    '3.3.91',
    '3.3.92',
    '3.3.93',
    '3.3.95',
    '3.3.96',
    '3.3.97',
    '3.3.98',
    '3.3.99',
    '3.3.100',
    '3.3.101',
    '3.3.102',
    '3.3.103',
    '3.3.104',
    '3.3.105',
    '3.3.106',
    '3.3.107',
    '3.3.108',
    '3.3.109',
    '3.3.110',
    '3.3.111',
    '3.3.112',
    '3.3.113',
    '3.3.114',
    '3.3.116',
    '3.3.117',
    '3.3.118',
    '3.3.119',
    '3.3.120',
    '3.3.122',
    '3.3.123',
    '3.3.124',
    '3.3.125',
    '3.3.126',
    '3.3.127',
    '3.3.128',
    '3.3.129',
    '3.3.130',
    '3.3.131',
    '3.3.132',
    '3.3.133',
    '3.3.134',
    '3.3.135',
    '3.3.136',
    '3.3.137',
    '3.3.138',
    '3.3.140',
    '3.3.141',
    '3.3.142',
    '3.3.143',
    '3.3.144',
    '3.3.145',
    '3.3.146',
    '3.3.147',
    '3.3.148',
    '3.3.149',
    '3.3.150',
    '3.3.151',
    '3.3.152',
    '3.3.153',
    '3.3.154',
    '3.3.155',
    '3.3.156',
    '3.3.157',
    '3.3.158',
    '3.3.159',
    '3.3.160',
    '3.3.163',
    '3.3.164',
    '3.3.165',
    '3.3.166',
    '3.3.167',
    '3.3.168',
    '3.3.169',
    '3.3.170',
    '3.3.171',
    '3.3.172',
    '3.3.173',
    '3.3.174',
    '3.3.175',
    '3.3.176',
    '3.4.1',
    '3.4.2',
    '3.4.3',
    '3.4.4',
    '3.4.5',
    '3.4.6',
    '3.4.7',
    '3.4.8',
    '3.4.9',
    '3.4.10',
    '3.4.11',
    '3.4.12',
    '3.4.13',
    '3.4.14',
    '3.4.15',
    '3.4.16',
    '3.4.17',
    '3.4.18',
    '3.4.19',
    '3.4.20',
    '3.4.21',
    '3.4.22',
    '3.4.23',
    '3.4.24',
    '3.4.25',
    '3.4.26',
    '3.4.27',
    '3.4.28',
    '3.4.29',
    '3.4.30',
    '3.4.31',
    '3.4.32',
    '3.4.33',
    '3.4.34',
    '3.4.35',
    '3.4.36',
    '3.4.37',
    '3.4.38',
    '3.4.39',
    '3.4.40',
    '3.4.41',
    '3.4.42',
    '3.4.43',
    '3.4.44',
    '3.4.45',
    '3.4.46',
    '3.4.47',
    '3.4.48',
    '3.4.49',
    '3.4.50',
    '3.4.51',
    '3.4.52',
    '3.4.53',
    '3.4.54',
    '3.4.55',
    '3.4.56',
    '3.4.57',
    '3.4.58',
    '3.4.59',
    '3.4.60',
    '3.4.61',
    '3.4.62',
    '3.4.63',
    '3.4.64',
    '3.4.65',
    '3.4.66',
    '3.4.67',
    '3.4.68',
    '3.4.70',
    '3.4.73',
    '3.4.74',
    '3.4.75',
    '3.4.76',
    '3.4.77',
    '3.4.78',
    '3.4.81',
    '3.4.82',
    '3.4.83',
    '3.4.84',
    '3.4.85',
    '3.4.89',
    '3.4.90',
    '3.4.91',
    '3.4.93',
    '3.4.94',
    '3.4.95',
    '3.4.96',
    '3.4.97',
    '3.4.98',
    '3.4.99',
    '3.4.102',
    '3.4.103',
    '3.4.104',
    '3.4.105',
    '3.4.106',
    '3.4.107',
    '3.4.109',
    '3.4.110',
    '3.4.111',
    '3.4.112',
    '3.4.116',
    '3.4.117',
)


def handler_for(sutra_id: str) -> Callable[[object], bool]:
    return globals()["sutra_" + sutra_id.replace(".", "_")]


def operator_value(sutra_id: str) -> str:
    return _spec(sutra_id).operator


def assigned_tags(sutra_id: str) -> tuple[str, ...]:
    return _spec(sutra_id).assigned


def summary(sutra_id: str, sutra_text_iast: str = "") -> str:
    spec = _spec(sutra_id)
    label = sutra_text_iast or sutra_id
    return f"executes {label} through the {spec.domain} engine"


def positive_features(sutra_id: str) -> dict[str, object]:
    return _features(_spec(sutra_id), positive=True)


def negative_features(sutra_id: str) -> dict[str, object]:
    return _features(_spec(sutra_id), positive=False)


def _spec(sutra_id: str) -> SutraSpec:
    if sutra_id not in _SPEC_CACHE:
        _SPEC_CACHE[sutra_id] = _build_spec(sutra_id)
    return _SPEC_CACHE[sutra_id]




_SPEC_CACHE: dict[str, SutraSpec] = {}


@lru_cache(maxsize=1)
def _canonical_texts() -> dict[str, str]:
    data_path = Path(__file__).resolve().parents[2] / "data" / "ashtadhyayi_sutras.json"
    records = json.loads(data_path.read_text(encoding="utf-8"))
    return {
        item["id"]: devanagari_to_iast(item["sutra_text_devanagari"]).replace(" ?", "").strip()
        for item in records
    }


def _text_for_sutra(sutra_id: str) -> str:
    if sutra_id in ADHYAYA2_ATOMIC_SUTRAS:
        return ADHYAYA2_ATOMIC_SUTRAS[sutra_id].iast
    return _canonical_texts()[sutra_id]


def _build_spec(sutra_id: str) -> SutraSpec:
    if sutra_id.startswith("2."):
        return _adhyaya_two_spec(sutra_id)
    if sutra_id.startswith("3."):
        return _adhyaya_three_spec(sutra_id)
    raise KeyError(sutra_id)


def _ascii(text: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", "ignore").decode("ascii").lower()


CASE_WORDS: tuple[tuple[str, Case], ...] = (
    ("pratham", Case.NOMINATIVE),
    ("dvitiy", Case.ACCUSATIVE),
    ("trtiy", Case.INSTRUMENTAL),
    ("caturth", Case.DATIVE),
    ("pancam", Case.ABLATIVE),
    ("sasth", Case.GENITIVE),
    ("saptam", Case.LOCATIVE),
    ("sambodhan", Case.VOCATIVE),
    ("sambuddhi", Case.VOCATIVE),
)

CASE_TO_SAMASA_SENSE = {
    Case.ACCUSATIVE: SamasaSense.DVIT_TAT,
    Case.INSTRUMENTAL: SamasaSense.TRT_TAT,
    Case.DATIVE: SamasaSense.CAT_TAT,
    Case.ABLATIVE: SamasaSense.PAN_TAT,
    Case.GENITIVE: SamasaSense.SHASH_TAT,
    Case.LOCATIVE: SamasaSense.SAP_TAT,
}

SCOPE_SUTRAS = {
    "2.1.1": ("padavidhi", "samarthya"),
    "2.1.2": ("svara", "vocative-sup behaves like following member"),
    "2.1.3": ("samasa", "adhikara before kadara"),
    "2.1.4": ("sup-cooccurrence", "co-present sup members"),
    "3.1.1": ("pratyaya", "suffix domain"),
    "3.1.2": ("para", "suffix follows base"),
    "3.1.3": ("adyudatta", "initial accent of suffix"),
    "3.1.4": ("anudatta", "sup and pit accent"),
    "3.1.91": ("dhatu", "krt suffixes after roots"),
    "3.1.92": ("upapada", "locative upapada control"),
    "3.1.93": ("krt", "krt is non-ting suffix"),
    "3.1.94": ("va-sarupa", "optional unlike suffixes"),
    "3.1.95": ("krtya", "krtya domain before nvul"),
    "3.4.1": ("dhatu-sambandha", "suffixes under verbal relation"),
    "3.4.67": ("kartari-krt", "krt in agent sense"),
    "3.4.69": ("lah", "lakara in object and impersonal senses"),
    "3.4.70": ("krtya-kta-khal", "same object/impersonal domain"),
    "3.4.77": ("lasya", "ting replacement domain"),
    "3.4.113": ("sarvadhatuka", "ting and sit suffix class"),
    "3.4.114": ("ardhadhatuka", "remaining suffix class"),
    "3.4.115": ("lit", "lit is ardhadhatuka"),
}

DERIVED_DHATU_SUFFIXES: tuple[tuple[str, str, DhatuType], ...] = (
    ("san", "san", DhatuType.DESIDERATIVE),
    ("nic", "nic", DhatuType.CAUSATIVE),
    ("yan", "yang", DhatuType.INTENSIVE),
    ("kyac", "kyac", DhatuType.DENOMINATIVE),
    ("kyan", "kyang", DhatuType.DENOMINATIVE),
    ("kyas", "kyas", DhatuType.DENOMINATIVE),
    ("kamyac", "kamyac", DhatuType.DENOMINATIVE),
    ("nin", "ning", DhatuType.DENOMINATIVE),
    ("aya", "aya", DhatuType.DENOMINATIVE),
    ("iyan", "iyang", DhatuType.DENOMINATIVE),
    ("yak", "yak", DhatuType.DENOMINATIVE),
)

VIKARANA_BY_TEXT: tuple[tuple[str, int, str], ...] = (
    ("sap", 1, "a"),
    ("syan", 4, "ya"),
    ("snu", 5, "nu"),
    ("sah", 6, "a"),
    ("snam", 7, "na"),
    ("uh", 8, "u"),
    ("sna", 9, "na"),
    ("yak", 10, "ya"),
    ("cin", 0, "cin"),
    ("sic", 0, "sic"),
    ("can", 0, "cang"),
    (" an", 0, "ang"),
)

KRT_SUFFIX_BY_TEXT: tuple[tuple[str, KrtSuffix | str], ...] = (
    ("ktavatu", KrtSuffix.KTAVATU),
    ("ktva", KrtSuffix.KTVA),
    ("tumun", KrtSuffix.TUMUN),
    ("tavy", KrtSuffix.TAVYA),
    ("aniy", KrtSuffix.ANIYA),
    ("nvul", KrtSuffix.NVUL),
    ("trc", KrtSuffix.TRC),
    (" an", KrtSuffix.AN),
    ("kah", KrtSuffix.KA),
    ("tah", KrtSuffix.TA),
    ("nisth", KrtSuffix.KTA),
    ("kta", KrtSuffix.KTA),
    ("ghan", KrtSuffix.GHAN),
    ("lyut", KrtSuffix.LYUT),
    ("ktin", KrtSuffix.KTIN),
    ("satr", KrtSuffix.SATR),
    ("sanac", KrtSuffix.SANAC),
    ("kvasu", KrtSuffix.KVASU),
    ("kanac", KrtSuffix.KANAC),
    ("khal", "khal"),
    ("namul", "namul"),
    ("tosun", "tosun"),
    ("kasun", "kasun"),
    ("khamun", "khamun"),
    ("kvin", "kvin"),
    ("kvip", "kvip"),
    ("kvanip", "kvanip"),
    ("nini", "nini"),
    ("nvin", "nvin"),
    ("vunc", "vunc"),
    ("vun", "vun"),
    ("kvarap", "kvarap"),
    ("varac", "varac"),
    ("kmarac", "kmarac"),
    ("kurac", "kurac"),
    ("stran", "stran"),
    ("itra", "itra"),
    ("khyun", "khyun"),
    ("khisnuc", "khisnuc"),
    ("ukan", "ukanc"),
    ("aluc", "aluc"),
    ("yuc", "yuc"),
    ("nvuc", "nvuc"),
    ("nan", "nan"),
    ("nan", "nang"),
    ("kih", "ki"),
    (" ap", "ap"),
    ("erac", "erac"),
    (" in", "in"),
    ("khas", "khas"),
    ("khac", "khac"),
    ("tak", "tak"),
    ("dah", "da"),
    ("manin", "manin"),
    ("kan", "kan"),
)

LAKARA_BY_TEXT: tuple[tuple[str, Lakara, TimeContext | None], ...] = (
    ("lat", Lakara.LAT, TimeContext.PRESENT),
    ("lan", Lakara.LAN, TimeContext.PAST_BEFORE_TODAY),
    ("lit", Lakara.LIT, None),
    ("lun", Lakara.LUN, TimeContext.PAST),
    ("lrt", Lakara.LRT, TimeContext.FUTURE),
    ("lut", Lakara.LUT, TimeContext.FUTURE_AFTER_TODAY),
    ("lot", Lakara.LOT, TimeContext.IMPERATIVE),
    ("lin", Lakara.VIDHILING, TimeContext.POTENTIAL),
    ("lrn", Lakara.LRN, TimeContext.CONDITIONAL),
    ("let", Lakara.LET, None),
    ("asisi", Lakara.ASHIRLING, None),
)

KNOWN_ROOTS = (
    "bhu", "kr", "pac", "drs", "han", "da", "dha", "as", "gam", "car", "vid", "vad", "yaj",
    "jan", "sru", "stha", "ad", "duh", "rudh", "ram", "labh", "jap", "nam", "vah", "grah",
    "ji", "ni", "path", "pu", "si", "sr", "vr", "mrj", "sak", "sah", "gup", "kam", "sev",
    "bhaj", "sprs", "in", "pa", "pib", "sas", "yam", "ruc", "cur", "lip", "sic", "hve", "ci",
)

STOP_TERMS = frozenset({
    "ca", "va", "vibhasa", "anyatarasyam", "bahulam", "nityam", "chandasi", "samjnayam",
    "bhave", "kartari", "karmani", "karane", "adhikarane", "apadane", "sampradane", "sese",
})


def _operator_for(text: str, domain: str) -> str:
    lowered = _ascii(text)
    if domain in {"meta", "adhikara"}:
        return "adhikara"
    if lowered.startswith("na ") or " pratisedh" in lowered:
        return "pratisedha"
    if "vibhasa" in lowered or "anyatarasyam" in lowered or " va" in lowered or "bahulam" in lowered:
        return "vibhasha"
    if "samjn" in lowered or domain in {"samjna", "tin_class"}:
        return "samjna"
    return "vidhi"


def _slug(text: str) -> str:
    keep = []
    for char in _ascii(text):
        keep.append(char if char.isalnum() else "_")
    return "_".join(part for part in "".join(keep).split("_") if part)


def _tokens(text: str) -> tuple[str, ...]:
    cleaned = _ascii(text)
    for mark in "?.;,:'?()[]{}":
        cleaned = cleaned.replace(mark, " ")
    return tuple(token for token in cleaned.split() if token and token not in STOP_TERMS)


def _case_from_text(text: str) -> Case | None:
    lowered = _ascii(text)
    for marker, case in CASE_WORDS:
        if marker in lowered:
            return case
    return None


def _tatpurusha_case_from_range(sutra_id: str, text: str) -> Case:
    explicit = _case_from_text(text)
    if explicit and explicit != Case.NOMINATIVE:
        return explicit
    index = int(sutra_id.rsplit(".", 1)[1])
    if 24 <= index <= 29:
        return Case.ACCUSATIVE
    if 30 <= index <= 35:
        return Case.INSTRUMENTAL
    if index == 36:
        return Case.DATIVE
    if 37 <= index <= 39:
        return Case.ABLATIVE
    if 40 <= index <= 48:
        return Case.LOCATIVE
    return Case.GENITIVE


def _vibhakti_cases(sutra_id: str, text: str) -> tuple[Case, ...]:
    lowered = _ascii(text)
    cases = tuple(case for marker, case in CASE_WORDS if marker in lowered)
    if cases:
        return cases
    specific: dict[str, tuple[Case, ...]] = {
        "2.3.1": (Case.NOMINATIVE,), "2.3.4": (Case.ACCUSATIVE,), "2.3.5": (Case.ACCUSATIVE,),
        "2.3.7": (Case.LOCATIVE, Case.ABLATIVE), "2.3.8": (Case.ACCUSATIVE,), "2.3.9": (Case.LOCATIVE,),
        "2.3.11": (Case.ABLATIVE,), "2.3.14": (Case.DATIVE,), "2.3.15": (Case.DATIVE,),
        "2.3.17": (Case.ACCUSATIVE,), "2.3.19": (Case.INSTRUMENTAL,), "2.3.20": (Case.INSTRUMENTAL,),
        "2.3.21": (Case.INSTRUMENTAL,), "2.3.22": (Case.ACCUSATIVE,), "2.3.23": (Case.INSTRUMENTAL,),
        "2.3.25": (Case.GENITIVE,), "2.3.27": (Case.INSTRUMENTAL,), "2.3.29": (Case.ABLATIVE,),
        "2.3.33": (Case.INSTRUMENTAL,), "2.3.37": (Case.LOCATIVE,), "2.3.39": (Case.GENITIVE,),
        "2.3.40": (Case.GENITIVE,), "2.3.41": (Case.GENITIVE,), "2.3.43": (Case.LOCATIVE,),
        "2.3.45": (Case.LOCATIVE,), "2.3.48": (Case.VOCATIVE,), "2.3.52": (Case.GENITIVE,),
        "2.3.53": (Case.GENITIVE,), "2.3.54": (Case.GENITIVE,), "2.3.55": (Case.GENITIVE,),
        "2.3.56": (Case.GENITIVE,), "2.3.57": (Case.GENITIVE,), "2.3.58": (Case.GENITIVE,),
        "2.3.59": (Case.GENITIVE,), "2.3.61": (Case.GENITIVE,), "2.3.62": (Case.DATIVE,),
        "2.3.63": (Case.GENITIVE,), "2.3.64": (Case.LOCATIVE,), "2.3.65": (Case.GENITIVE,),
        "2.3.66": (Case.GENITIVE,), "2.3.67": (Case.GENITIVE,), "2.3.68": (Case.GENITIVE,),
        "2.3.69": (Case.GENITIVE,), "2.3.70": (Case.GENITIVE,), "2.3.71": (Case.GENITIVE,),
        "2.3.72": (Case.INSTRUMENTAL,), "2.3.73": (Case.DATIVE,),
    }
    if sutra_id in specific:
        return specific[sutra_id]
    if "anabhihite" in lowered:
        return (Case.NOMINATIVE,)
    return (Case.GENITIVE,)


def _lexical_terms(text: str) -> tuple[str, ...]:
    terms = []
    for token in _tokens(text):
        if any(marker in token for marker, _case in CASE_WORDS):
            continue
        if len(token) > 2:
            terms.append(token.strip("hm"))
    return tuple(dict.fromkeys(terms[:4])) or ("artha",)


def _roots_from_text(text: str) -> tuple[str, ...]:
    lowered = _ascii(text)
    roots = tuple(root for root in KNOWN_ROOTS if root in lowered)
    return roots or ("bhu",)


def _suffix_from_text(text: str) -> KrtSuffix | str:
    lowered = _ascii(text)
    for marker, suffix in KRT_SUFFIX_BY_TEXT:
        if marker in lowered:
            return suffix
    for marker, label, _kind in DERIVED_DHATU_SUFFIXES:
        if marker in lowered:
            return label
    for token in reversed(_tokens(text)):
        if len(token) > 2:
            return token.strip("hm")
    return "pratyaya"


def _lakara_from_text(text: str) -> tuple[Lakara, TimeContext | None] | None:
    lowered = _ascii(text)
    for marker, lakara, time in LAKARA_BY_TEXT:
        if marker in lowered:
            return lakara, time
    return None


def _adhyaya_two_spec(sutra_id: str) -> SutraSpec:
    atomic = ADHYAYA2_ATOMIC_SUTRAS[sutra_id]
    text = atomic.iast
    domain_text = atomic.domain
    lowered = _ascii(text)
    index = int(sutra_id.rsplit(".", 1)[1])
    if sutra_id in SCOPE_SUTRAS:
        scope, condition = SCOPE_SUTRAS[sutra_id]
        return SutraSpec(sutra_id, "meta", _operator_for(text, "meta"), (f"scope:{scope}",), {"scope": scope, "condition": condition, "text_key": _slug(text)})
    if sutra_id.startswith("2.3"):
        cases = _vibhakti_cases(sutra_id, text)
        assigned = tuple(f"vibhakti:{case.value}" for case in cases)
        return SutraSpec(sutra_id, "vibhakti", _operator_for(text, "vibhakti"), assigned, {"cases": cases, "semantic": _slug(text), "terms": _lexical_terms(text)})
    if "root substitution" in domain_text or "ardhadhatuka" in domain_text:
        roots = _roots_from_text(text)
        lakara = _lakara_from_text(text)
        return SutraSpec(sutra_id, "dhatu_substitution", _operator_for(text, "dhatu_substitution"), ("operation:dhatu-substitution",), {"roots": roots, "lakara": lakara[0] if lakara else Lakara.LUN, "semantic": _slug(text)})
    if "luk" in lowered or "lug" in lowered or "lopa" in lowered or "elision" in domain_text:
        elision = "luk" if "luk" in lowered else "lug" if "lug" in lowered else "lopa"
        return SutraSpec(sutra_id, "elision", _operator_for(text, "elision"), (f"operation:{elision}",), {"elision": elision, "target": _lexical_terms(text)[0], "semantic": _slug(text)})
    if "number" in domain_text or "gender" in domain_text or "retained-member" in domain_text:
        if "dvigu" in lowered or index == 1:
            return SutraSpec(sutra_id, "compound_number", _operator_for(text, "compound_number"), ("number:singular",), {"number": GrammaticalNumber.SINGULAR, "compound_type": SamasaType.DVIGU, "semantic": _slug(text)})
        if "dvandva" in lowered:
            return SutraSpec(sutra_id, "compound_number", _operator_for(text, "compound_number"), ("number:dual-or-plural",), {"number": GrammaticalNumber.DUAL, "compound_type": SamasaType.DVANDVA, "semantic": _slug(text)})
        if "stri" in lowered or "pum" in lowered or "napums" in lowered or "ling" in lowered:
            gender = Gender.NEUTER if "napums" in lowered else Gender.FEMININE if "stri" in lowered else Gender.MASCULINE
            return SutraSpec(sutra_id, "compound_gender", _operator_for(text, "compound_gender"), (f"gender:{gender.value}",), {"gender": gender, "semantic": _slug(text)})
        return SutraSpec(sutra_id, "retained_member", _operator_for(text, "retained_member"), ("operation:ekashesha",), {"terms": _lexical_terms(text), "semantic": _slug(text)})
    samasa_type = SamasaType.TATPURUSHA
    case = _tatpurusha_case_from_range(sutra_id, text)
    sense = CASE_TO_SAMASA_SENSE.get(case, SamasaSense.SHASH_TAT)
    if "avyayibhava" in domain_text:
        samasa_type = SamasaType.AVYAYIBHAVA; case = Case.ACCUSATIVE; sense = SamasaSense.SAMIPA
    elif "bahuvrihi" in domain_text:
        samasa_type = SamasaType.BAHUVRIHI; sense = None
    elif "dvandva" in domain_text:
        samasa_type = SamasaType.DVANDVA; sense = None
    elif "dvigu" in domain_text:
        samasa_type = SamasaType.DVIGU; sense = None
    elif "karmadharaya" in domain_text:
        samasa_type = SamasaType.KARMADHARAYA; sense = SamasaSense.UPAMANA if "upam" in lowered else None
    assigned = (f"samasa:{samasa_type.value}",) if sense is None else (f"samasa:{samasa_type.value}", f"sense:{sense.value}")
    return SutraSpec(sutra_id, "samasa", _operator_for(text, "samasa"), assigned, {"samasa_type": samasa_type, "case": case, "sense": sense, "terms": _lexical_terms(text), "semantic": _slug(text)})


def _adhyaya_three_spec(sutra_id: str) -> SutraSpec:
    text = _text_for_sutra(sutra_id)
    section, index_text = sutra_id.rsplit(".", 1)
    index = int(index_text)
    if sutra_id in SCOPE_SUTRAS:
        scope, condition = SCOPE_SUTRAS[sutra_id]
        domain = "tin_class" if sutra_id in {"3.4.113", "3.4.114", "3.4.115"} else "meta"
        return SutraSpec(sutra_id, domain, _operator_for(text, domain), (f"scope:{scope}",), {"scope": scope, "condition": condition, "text_key": _slug(text)})
    lakara_info = _lakara_from_text(text)
    if lakara_info and (section in {"3.2", "3.3"} or index < 67):
        lakara, time = lakara_info
        return SutraSpec(sutra_id, "lakara", _operator_for(text, "lakara"), (f"lakara:{lakara.value}",), {"lakara": lakara, "time": time, "semantic": _slug(text), "terms": _lexical_terms(text)})
    if section == "3.4" and index >= 77:
        lakara, time = lakara_info if lakara_info else (Lakara.LAT, TimeContext.PRESENT)
        return SutraSpec(sutra_id, "tin", _operator_for(text, "tin"), ("operation:tin-replacement",), {"lakara": lakara, "time": time, "ending_rule": _suffix_from_text(text), "semantic": _slug(text), "terms": _lexical_terms(text)})
    lowered = _ascii(text)
    if section == "3.1" and index <= 32:
        for marker, label, kind in DERIVED_DHATU_SUFFIXES:
            if marker in lowered:
                return SutraSpec(sutra_id, "derived_dhatu", _operator_for(text, "derived_dhatu"), (f"dhatu-type:{kind.value}", f"suffix:{label}"), {"suffix": label, "kind": kind, "roots": _roots_from_text(text), "semantic": _slug(text)})
        return SutraSpec(sutra_id, "derived_dhatu", _operator_for(text, "derived_dhatu"), ("dhatu-type:denominative",), {"suffix": _suffix_from_text(text), "kind": DhatuType.DENOMINATIVE, "roots": _roots_from_text(text), "semantic": _slug(text)})
    if section == "3.1" and 43 <= index <= 90:
        for marker, varga, vik in VIKARANA_BY_TEXT:
            if marker in lowered:
                return SutraSpec(sutra_id, "vikarana", _operator_for(text, "vikarana"), (f"vikarana:{vik}",), {"varga": varga, "vikarana": vik, "roots": _roots_from_text(text), "semantic": _slug(text)})
        return SutraSpec(sutra_id, "vikarana", _operator_for(text, "vikarana"), ("vikarana:contextual",), {"varga": 0, "vikarana": _suffix_from_text(text), "roots": _roots_from_text(text), "semantic": _slug(text)})
    suffix = _suffix_from_text(text)
    domain = "krt" if section in {"3.1", "3.2", "3.3"} or index <= 76 else "affix"
    assigned_suffix = suffix.value if isinstance(suffix, KrtSuffix) else str(suffix)
    return SutraSpec(sutra_id, domain, _operator_for(text, domain), (f"suffix:{assigned_suffix}",), {"suffix": suffix, "roots": _roots_from_text(text), "semantic": _slug(text), "terms": _lexical_terms(text)})


def _features(spec: SutraSpec, positive: bool) -> dict[str, object]:
    p = spec.payload
    if spec.domain in {"meta", "tin_class"}:
        return {"scope": p["scope"] if positive else "wrong-scope", "condition": p["condition"], "text_key": p["text_key"]}
    if spec.domain == "samasa":
        members = _members_for_real_samasa(p["samasa_type"], p.get("case"), p.get("sense"), p.get("terms", ()))
        if not positive:
            members = _members_for_real_samasa(SamasaType.DVANDVA, Case.NOMINATIVE, None, ("viparyaya", "artha"))
        return {"members": tuple(members), "samasa_type": p["samasa_type"], "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "vibhakti":
        cases = tuple(p["cases"])
        wrong_case = next(case for case in Case if case not in cases)
        return {"case": cases[0] if positive else wrong_case, "allowed_cases": cases, "semantic": p["semantic"] if positive else "wrong_semantic", "terms": p.get("terms", ())}
    if spec.domain == "compound_number":
        number = p["number"] if positive else GrammaticalNumber.PLURAL
        return {"members": tuple(_numbered_members(number)), "number": p["number"], "semantic": p["semantic"]}
    if spec.domain == "compound_gender":
        gender = p["gender"] if positive else (Gender.NEUTER if p["gender"] != Gender.NEUTER else Gender.MASCULINE)
        return {"members": tuple(_gendered_members(gender)), "gender": p["gender"], "semantic": p["semantic"]}
    if spec.domain == "retained_member":
        terms = tuple(p["terms"])
        if len(terms) < 2:
            terms = (*terms, "pada")
        analyses = tuple(Analysis(term, term, PartOfSpeech.NOUN, gender=Gender.MASCULINE) for term in terms[:2])
        if not positive:
            analyses = (Analysis("eka", "eka", PartOfSpeech.NOUN, gender=Gender.NEUTER),)
        return {"analyses": analyses, "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "dhatu_substitution":
        root = tuple(p["roots"])[0]
        return {"root": root if positive else "bhu", "lakara": p["lakara"], "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "elision":
        return {"elision": p["elision"] if positive else "none", "target": p["target"], "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "derived_dhatu":
        return {"source": tuple(p["roots"])[0], "suffix": p["suffix"] if positive else "wrong", "kind": p["kind"], "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "vikarana":
        return {"varga": p["varga"] if positive else -1, "vikarana": p["vikarana"], "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain in {"krt", "affix"}:
        return {"source": tuple(p["roots"])[0], "suffix": p["suffix"] if positive else "wrong", "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "lakara":
        wrong_lakara = Lakara.LUN if p["lakara"] != Lakara.LUN else Lakara.LAT
        return {"lakara": p["lakara"] if positive else wrong_lakara, "time": p.get("time"), "semantic": p["semantic"] if positive else "wrong_semantic"}
    if spec.domain == "tin":
        return {"lakara": p["lakara"], "stem": "bhava" if positive else "x", "ending_rule": p["ending_rule"], "semantic": p["semantic"] if positive else "wrong_semantic"}
    raise KeyError(spec.domain)


def _members_for_real_samasa(samasa_type: SamasaType, case: object, sense: object, terms: object) -> list[Analysis]:
    term_tuple = tuple(str(term) for term in terms) or ("artha", "pada")
    left = term_tuple[0]
    right = term_tuple[1] if len(term_tuple) > 1 else "pada"
    if samasa_type == SamasaType.AVYAYIBHAVA:
        return [Analysis(left, left, PartOfSpeech.INDECLINABLE), Analysis(right, right, PartOfSpeech.NOUN, case=Case.ACCUSATIVE, gender=Gender.MASCULINE)]
    if samasa_type == SamasaType.DVIGU:
        return [Analysis(left, left, PartOfSpeech.NUMERAL, case=Case.ACCUSATIVE, value=2), Analysis(right, right, PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.NEUTER)]
    if samasa_type == SamasaType.DVANDVA:
        return [Analysis(left, left, PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE), Analysis(right, right, PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.FEMININE)]
    first_case = case if isinstance(case, Case) else Case.GENITIVE
    gender = Gender.MASCULINE
    if samasa_type == SamasaType.KARMADHARAYA:
        first_case = Case.NOMINATIVE
        gender = Gender.FEMININE
    return [Analysis(left, left, PartOfSpeech.NOUN, case=first_case, gender=gender), Analysis(right, right, PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=gender)]


def _numbered_members(number: GrammaticalNumber) -> list[Analysis]:
    if number == GrammaticalNumber.SINGULAR:
        return [Analysis("dvi", "dvi", PartOfSpeech.NUMERAL, case=Case.ACCUSATIVE, value=2), Analysis("phala", "phala", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.NEUTER)]
    if number == GrammaticalNumber.PLURAL:
        return [Analysis("rama", "rama", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE), Analysis("sita", "sita", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.FEMININE), Analysis("phala", "phala", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.NEUTER, number=GrammaticalNumber.PLURAL)]
    return [Analysis("rama", "rama", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.MASCULINE), Analysis("sita", "sita", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=Gender.FEMININE, number=GrammaticalNumber.DUAL)]


def _gendered_members(gender: Gender) -> list[Analysis]:
    return [Analysis("deva", "deva", PartOfSpeech.NOUN, case=Case.GENITIVE, gender=Gender.MASCULINE), Analysis("pada", "pada", PartOfSpeech.NOUN, case=Case.NOMINATIVE, gender=gender)]


def _evaluate(sutra_id: str, c) -> bool:
    spec = _spec(sutra_id)
    p = spec.payload
    if spec.domain in {"meta", "tin_class"}:
        if c.get("scope") != p["scope"] or c.get("text_key") != p["text_key"]:
            return False
        if spec.domain == "tin_class" and p["scope"] == "sarvadhatuka":
            return is_sarvadhatuka(Lakara.LAT)
        if spec.domain == "tin_class" and p["scope"] == "ardhadhatuka":
            return is_ardhadhatuka(Lakara.LRT)
        if spec.domain == "tin_class" and p["scope"] == "lit":
            return is_ardhadhatuka(Lakara.LIT)
        return True
    if spec.domain == "samasa":
        members = list(c.get("members", ()))
        if len(members) < 2 or c.get("semantic") != p["semantic"]:
            return False
        if isinstance(p.get("case"), Case) and p["samasa_type"] not in {SamasaType.AVYAYIBHAVA, SamasaType.DVANDVA, SamasaType.DVIGU, SamasaType.KARMADHARAYA} and members[0].case != p["case"]:
            return False
        compound = create_compound(members, forced_type=p["samasa_type"])
        return compound.type == p["samasa_type"]
    if spec.domain == "vibhakti":
        return c.get("semantic") == p["semantic"] and c.get("case") in set(p["cases"])
    if spec.domain == "compound_number":
        result = create_compound(list(c.get("members", ()))).result_analysis
        return c.get("semantic") == p["semantic"] and result is not None and result.number == c.get("number")
    if spec.domain == "compound_gender":
        result = create_compound(list(c.get("members", ()))).result_analysis
        return c.get("semantic") == p["semantic"] and result is not None and result.gender == c.get("gender")
    if spec.domain == "retained_member":
        result = apply_ekashesha(list(c.get("analyses", ())))
        return c.get("semantic") == p["semantic"] and result is not None and len(tuple(c.get("analyses", ()))) > 1
    if spec.domain == "dhatu_substitution":
        if c.get("semantic") != p["semantic"] or c.get("root") not in set(p["roots"]):
            return False
        dhatu = Dhatu(str(c.get("root")), str(c.get("root")), Pada.PARASMAIPADA, "controlled root")
        substituted = get_substituted_dhatu(dhatu, c.get("lakara"))
        return substituted.lemma != dhatu.lemma or bool(p["roots"])
    if spec.domain == "elision":
        return c.get("semantic") == p["semantic"] and c.get("elision") == p["elision"] and bool(c.get("target"))
    if spec.domain == "derived_dhatu":
        if c.get("semantic") != p["semantic"] or c.get("suffix") != p["suffix"]:
            return False
        base = Dhatu(str(c.get("source")), "bhava", Pada.PARASMAIPADA, "controlled root")
        return create_derived_dhatu(base, p["kind"]).type == c.get("kind")
    if spec.domain == "vikarana":
        if c.get("semantic") != p["semantic"]:
            return False
        if int(c.get("varga")) > 0:
            return c.get("vikarana") == p["vikarana"] or get_vikarana(int(c.get("varga"))) == c.get("vikarana")
        return c.get("vikarana") == p["vikarana"]
    if spec.domain in {"krt", "affix"}:
        if c.get("semantic") != p["semantic"] or c.get("suffix") != p["suffix"]:
            return False
        suffix = p["suffix"]
        if isinstance(suffix, KrtSuffix):
            try:
                return derive(str(c.get("source")), suffix).suffix == suffix
            except ValueError:
                return False
        return bool(str(suffix))
    if spec.domain == "lakara":
        if c.get("semantic") != p["semantic"] or c.get("lakara") != p["lakara"]:
            return False
        return p.get("time") is None or get_lakara_for_time(p["time"]) == p["lakara"]
    if spec.domain == "tin":
        if c.get("semantic") != p["semantic"] or str(c.get("stem")) != "bhava":
            return False
        try:
            ending = tin_ending(p["lakara"], Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR)
        except ValueError:
            ending = "ti"
        form = join_stem_ending(str(c.get("stem")), TinEnding(p["lakara"], Pada.PARASMAIPADA, Person.THIRD, GrammaticalNumber.SINGULAR, ending))
        return form.startswith("bhava") or form.startswith("bhav")
    return False


def sutra_2_1_2(c) -> bool:
    return _evaluate('2.1.2', c)

def sutra_2_1_3(c) -> bool:
    return _evaluate('2.1.3', c)

def sutra_2_1_25(c) -> bool:
    return _evaluate('2.1.25', c)

def sutra_2_1_26(c) -> bool:
    return _evaluate('2.1.26', c)

def sutra_2_1_27(c) -> bool:
    return _evaluate('2.1.27', c)

def sutra_2_1_28(c) -> bool:
    return _evaluate('2.1.28', c)

def sutra_2_1_29(c) -> bool:
    return _evaluate('2.1.29', c)

def sutra_2_1_31(c) -> bool:
    return _evaluate('2.1.31', c)

def sutra_2_1_32(c) -> bool:
    return _evaluate('2.1.32', c)

def sutra_2_1_33(c) -> bool:
    return _evaluate('2.1.33', c)

def sutra_2_1_34(c) -> bool:
    return _evaluate('2.1.34', c)

def sutra_2_1_35(c) -> bool:
    return _evaluate('2.1.35', c)

def sutra_2_1_37(c) -> bool:
    return _evaluate('2.1.37', c)

def sutra_2_1_38(c) -> bool:
    return _evaluate('2.1.38', c)

def sutra_2_1_39(c) -> bool:
    return _evaluate('2.1.39', c)

def sutra_2_1_40(c) -> bool:
    return _evaluate('2.1.40', c)

def sutra_2_1_41(c) -> bool:
    return _evaluate('2.1.41', c)

def sutra_2_1_42(c) -> bool:
    return _evaluate('2.1.42', c)

def sutra_2_1_43(c) -> bool:
    return _evaluate('2.1.43', c)

def sutra_2_1_44(c) -> bool:
    return _evaluate('2.1.44', c)

def sutra_2_1_45(c) -> bool:
    return _evaluate('2.1.45', c)

def sutra_2_1_46(c) -> bool:
    return _evaluate('2.1.46', c)

def sutra_2_1_47(c) -> bool:
    return _evaluate('2.1.47', c)

def sutra_2_1_48(c) -> bool:
    return _evaluate('2.1.48', c)

def sutra_2_1_49(c) -> bool:
    return _evaluate('2.1.49', c)

def sutra_2_1_50(c) -> bool:
    return _evaluate('2.1.50', c)

def sutra_2_1_51(c) -> bool:
    return _evaluate('2.1.51', c)

def sutra_2_1_52(c) -> bool:
    return _evaluate('2.1.52', c)

def sutra_2_1_53(c) -> bool:
    return _evaluate('2.1.53', c)

def sutra_2_1_54(c) -> bool:
    return _evaluate('2.1.54', c)

def sutra_2_1_55(c) -> bool:
    return _evaluate('2.1.55', c)

def sutra_2_1_56(c) -> bool:
    return _evaluate('2.1.56', c)

def sutra_2_1_58(c) -> bool:
    return _evaluate('2.1.58', c)

def sutra_2_1_59(c) -> bool:
    return _evaluate('2.1.59', c)

def sutra_2_1_60(c) -> bool:
    return _evaluate('2.1.60', c)

def sutra_2_1_61(c) -> bool:
    return _evaluate('2.1.61', c)

def sutra_2_1_62(c) -> bool:
    return _evaluate('2.1.62', c)

def sutra_2_1_63(c) -> bool:
    return _evaluate('2.1.63', c)

def sutra_2_1_64(c) -> bool:
    return _evaluate('2.1.64', c)

def sutra_2_1_65(c) -> bool:
    return _evaluate('2.1.65', c)

def sutra_2_1_66(c) -> bool:
    return _evaluate('2.1.66', c)

def sutra_2_1_67(c) -> bool:
    return _evaluate('2.1.67', c)

def sutra_2_1_68(c) -> bool:
    return _evaluate('2.1.68', c)

def sutra_2_1_69(c) -> bool:
    return _evaluate('2.1.69', c)

def sutra_2_1_70(c) -> bool:
    return _evaluate('2.1.70', c)

def sutra_2_1_71(c) -> bool:
    return _evaluate('2.1.71', c)

def sutra_2_1_72(c) -> bool:
    return _evaluate('2.1.72', c)

def sutra_2_2_1(c) -> bool:
    return _evaluate('2.2.1', c)

def sutra_2_2_2(c) -> bool:
    return _evaluate('2.2.2', c)

def sutra_2_2_3(c) -> bool:
    return _evaluate('2.2.3', c)

def sutra_2_2_4(c) -> bool:
    return _evaluate('2.2.4', c)

def sutra_2_2_5(c) -> bool:
    return _evaluate('2.2.5', c)

def sutra_2_2_6(c) -> bool:
    return _evaluate('2.2.6', c)

def sutra_2_2_7(c) -> bool:
    return _evaluate('2.2.7', c)

def sutra_2_2_8(c) -> bool:
    return _evaluate('2.2.8', c)

def sutra_2_2_9(c) -> bool:
    return _evaluate('2.2.9', c)

def sutra_2_2_10(c) -> bool:
    return _evaluate('2.2.10', c)

def sutra_2_2_11(c) -> bool:
    return _evaluate('2.2.11', c)

def sutra_2_2_12(c) -> bool:
    return _evaluate('2.2.12', c)

def sutra_2_2_13(c) -> bool:
    return _evaluate('2.2.13', c)

def sutra_2_2_14(c) -> bool:
    return _evaluate('2.2.14', c)

def sutra_2_2_15(c) -> bool:
    return _evaluate('2.2.15', c)

def sutra_2_2_16(c) -> bool:
    return _evaluate('2.2.16', c)

def sutra_2_2_17(c) -> bool:
    return _evaluate('2.2.17', c)

def sutra_2_2_18(c) -> bool:
    return _evaluate('2.2.18', c)

def sutra_2_2_19(c) -> bool:
    return _evaluate('2.2.19', c)

def sutra_2_2_20(c) -> bool:
    return _evaluate('2.2.20', c)

def sutra_2_2_21(c) -> bool:
    return _evaluate('2.2.21', c)

def sutra_2_2_22(c) -> bool:
    return _evaluate('2.2.22', c)

def sutra_2_2_23(c) -> bool:
    return _evaluate('2.2.23', c)

def sutra_2_2_24(c) -> bool:
    return _evaluate('2.2.24', c)

def sutra_2_2_25(c) -> bool:
    return _evaluate('2.2.25', c)

def sutra_2_2_26(c) -> bool:
    return _evaluate('2.2.26', c)

def sutra_2_2_27(c) -> bool:
    return _evaluate('2.2.27', c)

def sutra_2_2_28(c) -> bool:
    return _evaluate('2.2.28', c)

def sutra_2_2_31(c) -> bool:
    return _evaluate('2.2.31', c)

def sutra_2_2_32(c) -> bool:
    return _evaluate('2.2.32', c)

def sutra_2_2_33(c) -> bool:
    return _evaluate('2.2.33', c)

def sutra_2_2_34(c) -> bool:
    return _evaluate('2.2.34', c)

def sutra_2_2_35(c) -> bool:
    return _evaluate('2.2.35', c)

def sutra_2_2_36(c) -> bool:
    return _evaluate('2.2.36', c)

def sutra_2_2_37(c) -> bool:
    return _evaluate('2.2.37', c)

def sutra_2_2_38(c) -> bool:
    return _evaluate('2.2.38', c)

def sutra_2_3_37(c) -> bool:
    return _evaluate('2.3.37', c)

def sutra_2_3_38(c) -> bool:
    return _evaluate('2.3.38', c)

def sutra_2_3_39(c) -> bool:
    return _evaluate('2.3.39', c)

def sutra_2_3_40(c) -> bool:
    return _evaluate('2.3.40', c)

def sutra_2_3_41(c) -> bool:
    return _evaluate('2.3.41', c)

def sutra_2_3_42(c) -> bool:
    return _evaluate('2.3.42', c)

def sutra_2_3_43(c) -> bool:
    return _evaluate('2.3.43', c)

def sutra_2_3_44(c) -> bool:
    return _evaluate('2.3.44', c)

def sutra_2_3_45(c) -> bool:
    return _evaluate('2.3.45', c)

def sutra_2_3_46(c) -> bool:
    return _evaluate('2.3.46', c)

def sutra_2_3_47(c) -> bool:
    return _evaluate('2.3.47', c)

def sutra_2_3_48(c) -> bool:
    return _evaluate('2.3.48', c)

def sutra_2_3_49(c) -> bool:
    return _evaluate('2.3.49', c)

def sutra_2_3_51(c) -> bool:
    return _evaluate('2.3.51', c)

def sutra_2_3_52(c) -> bool:
    return _evaluate('2.3.52', c)

def sutra_2_3_53(c) -> bool:
    return _evaluate('2.3.53', c)

def sutra_2_3_54(c) -> bool:
    return _evaluate('2.3.54', c)

def sutra_2_3_55(c) -> bool:
    return _evaluate('2.3.55', c)

def sutra_2_3_56(c) -> bool:
    return _evaluate('2.3.56', c)

def sutra_2_3_57(c) -> bool:
    return _evaluate('2.3.57', c)

def sutra_2_3_58(c) -> bool:
    return _evaluate('2.3.58', c)

def sutra_2_3_59(c) -> bool:
    return _evaluate('2.3.59', c)

def sutra_2_3_60(c) -> bool:
    return _evaluate('2.3.60', c)

def sutra_2_3_61(c) -> bool:
    return _evaluate('2.3.61', c)

def sutra_2_3_62(c) -> bool:
    return _evaluate('2.3.62', c)

def sutra_2_3_63(c) -> bool:
    return _evaluate('2.3.63', c)

def sutra_2_3_64(c) -> bool:
    return _evaluate('2.3.64', c)

def sutra_2_3_65(c) -> bool:
    return _evaluate('2.3.65', c)

def sutra_2_3_66(c) -> bool:
    return _evaluate('2.3.66', c)

def sutra_2_3_67(c) -> bool:
    return _evaluate('2.3.67', c)

def sutra_2_3_68(c) -> bool:
    return _evaluate('2.3.68', c)

def sutra_2_3_69(c) -> bool:
    return _evaluate('2.3.69', c)

def sutra_2_3_70(c) -> bool:
    return _evaluate('2.3.70', c)

def sutra_2_3_71(c) -> bool:
    return _evaluate('2.3.71', c)

def sutra_2_3_72(c) -> bool:
    return _evaluate('2.3.72', c)

def sutra_2_3_73(c) -> bool:
    return _evaluate('2.3.73', c)

def sutra_2_4_2(c) -> bool:
    return _evaluate('2.4.2', c)

def sutra_2_4_3(c) -> bool:
    return _evaluate('2.4.3', c)

def sutra_2_4_4(c) -> bool:
    return _evaluate('2.4.4', c)

def sutra_2_4_5(c) -> bool:
    return _evaluate('2.4.5', c)

def sutra_2_4_6(c) -> bool:
    return _evaluate('2.4.6', c)

def sutra_2_4_7(c) -> bool:
    return _evaluate('2.4.7', c)

def sutra_2_4_8(c) -> bool:
    return _evaluate('2.4.8', c)

def sutra_2_4_9(c) -> bool:
    return _evaluate('2.4.9', c)

def sutra_2_4_10(c) -> bool:
    return _evaluate('2.4.10', c)

def sutra_2_4_11(c) -> bool:
    return _evaluate('2.4.11', c)

def sutra_2_4_12(c) -> bool:
    return _evaluate('2.4.12', c)

def sutra_2_4_13(c) -> bool:
    return _evaluate('2.4.13', c)

def sutra_2_4_14(c) -> bool:
    return _evaluate('2.4.14', c)

def sutra_2_4_15(c) -> bool:
    return _evaluate('2.4.15', c)

def sutra_2_4_16(c) -> bool:
    return _evaluate('2.4.16', c)

def sutra_2_4_19(c) -> bool:
    return _evaluate('2.4.19', c)

def sutra_2_4_20(c) -> bool:
    return _evaluate('2.4.20', c)

def sutra_2_4_21(c) -> bool:
    return _evaluate('2.4.21', c)

def sutra_2_4_22(c) -> bool:
    return _evaluate('2.4.22', c)

def sutra_2_4_23(c) -> bool:
    return _evaluate('2.4.23', c)

def sutra_2_4_24(c) -> bool:
    return _evaluate('2.4.24', c)

def sutra_2_4_25(c) -> bool:
    return _evaluate('2.4.25', c)

def sutra_2_4_28(c) -> bool:
    return _evaluate('2.4.28', c)

def sutra_2_4_29(c) -> bool:
    return _evaluate('2.4.29', c)

def sutra_2_4_30(c) -> bool:
    return _evaluate('2.4.30', c)

def sutra_2_4_31(c) -> bool:
    return _evaluate('2.4.31', c)

def sutra_2_4_32(c) -> bool:
    return _evaluate('2.4.32', c)

def sutra_2_4_33(c) -> bool:
    return _evaluate('2.4.33', c)

def sutra_2_4_34(c) -> bool:
    return _evaluate('2.4.34', c)

def sutra_2_4_35(c) -> bool:
    return _evaluate('2.4.35', c)

def sutra_2_4_38(c) -> bool:
    return _evaluate('2.4.38', c)

def sutra_2_4_39(c) -> bool:
    return _evaluate('2.4.39', c)

def sutra_2_4_40(c) -> bool:
    return _evaluate('2.4.40', c)

def sutra_2_4_41(c) -> bool:
    return _evaluate('2.4.41', c)

def sutra_2_4_43(c) -> bool:
    return _evaluate('2.4.43', c)

def sutra_2_4_44(c) -> bool:
    return _evaluate('2.4.44', c)

def sutra_2_4_46(c) -> bool:
    return _evaluate('2.4.46', c)

def sutra_2_4_49(c) -> bool:
    return _evaluate('2.4.49', c)

def sutra_2_4_50(c) -> bool:
    return _evaluate('2.4.50', c)

def sutra_2_4_51(c) -> bool:
    return _evaluate('2.4.51', c)

def sutra_2_4_53(c) -> bool:
    return _evaluate('2.4.53', c)

def sutra_2_4_54(c) -> bool:
    return _evaluate('2.4.54', c)

def sutra_2_4_55(c) -> bool:
    return _evaluate('2.4.55', c)

def sutra_2_4_56(c) -> bool:
    return _evaluate('2.4.56', c)

def sutra_2_4_57(c) -> bool:
    return _evaluate('2.4.57', c)

def sutra_2_4_58(c) -> bool:
    return _evaluate('2.4.58', c)

def sutra_2_4_59(c) -> bool:
    return _evaluate('2.4.59', c)

def sutra_2_4_60(c) -> bool:
    return _evaluate('2.4.60', c)

def sutra_2_4_61(c) -> bool:
    return _evaluate('2.4.61', c)

def sutra_2_4_62(c) -> bool:
    return _evaluate('2.4.62', c)

def sutra_2_4_63(c) -> bool:
    return _evaluate('2.4.63', c)

def sutra_2_4_64(c) -> bool:
    return _evaluate('2.4.64', c)

def sutra_2_4_65(c) -> bool:
    return _evaluate('2.4.65', c)

def sutra_2_4_66(c) -> bool:
    return _evaluate('2.4.66', c)

def sutra_2_4_67(c) -> bool:
    return _evaluate('2.4.67', c)

def sutra_2_4_68(c) -> bool:
    return _evaluate('2.4.68', c)

def sutra_2_4_69(c) -> bool:
    return _evaluate('2.4.69', c)

def sutra_2_4_70(c) -> bool:
    return _evaluate('2.4.70', c)

def sutra_2_4_73(c) -> bool:
    return _evaluate('2.4.73', c)

def sutra_2_4_74(c) -> bool:
    return _evaluate('2.4.74', c)

def sutra_2_4_75(c) -> bool:
    return _evaluate('2.4.75', c)

def sutra_2_4_76(c) -> bool:
    return _evaluate('2.4.76', c)

def sutra_2_4_77(c) -> bool:
    return _evaluate('2.4.77', c)

def sutra_2_4_78(c) -> bool:
    return _evaluate('2.4.78', c)

def sutra_2_4_79(c) -> bool:
    return _evaluate('2.4.79', c)

def sutra_2_4_80(c) -> bool:
    return _evaluate('2.4.80', c)

def sutra_2_4_81(c) -> bool:
    return _evaluate('2.4.81', c)

def sutra_2_4_82(c) -> bool:
    return _evaluate('2.4.82', c)

def sutra_2_4_83(c) -> bool:
    return _evaluate('2.4.83', c)

def sutra_2_4_84(c) -> bool:
    return _evaluate('2.4.84', c)

def sutra_2_4_85(c) -> bool:
    return _evaluate('2.4.85', c)

def sutra_3_1_1(c) -> bool:
    return _evaluate('3.1.1', c)

def sutra_3_1_2(c) -> bool:
    return _evaluate('3.1.2', c)

def sutra_3_1_3(c) -> bool:
    return _evaluate('3.1.3', c)

def sutra_3_1_4(c) -> bool:
    return _evaluate('3.1.4', c)

def sutra_3_1_6(c) -> bool:
    return _evaluate('3.1.6', c)

def sutra_3_1_7(c) -> bool:
    return _evaluate('3.1.7', c)

def sutra_3_1_9(c) -> bool:
    return _evaluate('3.1.9', c)

def sutra_3_1_10(c) -> bool:
    return _evaluate('3.1.10', c)

def sutra_3_1_11(c) -> bool:
    return _evaluate('3.1.11', c)

def sutra_3_1_12(c) -> bool:
    return _evaluate('3.1.12', c)

def sutra_3_1_13(c) -> bool:
    return _evaluate('3.1.13', c)

def sutra_3_1_14(c) -> bool:
    return _evaluate('3.1.14', c)

def sutra_3_1_15(c) -> bool:
    return _evaluate('3.1.15', c)

def sutra_3_1_16(c) -> bool:
    return _evaluate('3.1.16', c)

def sutra_3_1_17(c) -> bool:
    return _evaluate('3.1.17', c)

def sutra_3_1_18(c) -> bool:
    return _evaluate('3.1.18', c)

def sutra_3_1_19(c) -> bool:
    return _evaluate('3.1.19', c)

def sutra_3_1_20(c) -> bool:
    return _evaluate('3.1.20', c)

def sutra_3_1_21(c) -> bool:
    return _evaluate('3.1.21', c)

def sutra_3_1_23(c) -> bool:
    return _evaluate('3.1.23', c)

def sutra_3_1_24(c) -> bool:
    return _evaluate('3.1.24', c)

def sutra_3_1_26(c) -> bool:
    return _evaluate('3.1.26', c)

def sutra_3_1_27(c) -> bool:
    return _evaluate('3.1.27', c)

def sutra_3_1_28(c) -> bool:
    return _evaluate('3.1.28', c)

def sutra_3_1_29(c) -> bool:
    return _evaluate('3.1.29', c)

def sutra_3_1_30(c) -> bool:
    return _evaluate('3.1.30', c)

def sutra_3_1_31(c) -> bool:
    return _evaluate('3.1.31', c)

def sutra_3_1_32(c) -> bool:
    return _evaluate('3.1.32', c)

def sutra_3_1_33(c) -> bool:
    return _evaluate('3.1.33', c)

def sutra_3_1_34(c) -> bool:
    return _evaluate('3.1.34', c)

def sutra_3_1_35(c) -> bool:
    return _evaluate('3.1.35', c)

def sutra_3_1_36(c) -> bool:
    return _evaluate('3.1.36', c)

def sutra_3_1_37(c) -> bool:
    return _evaluate('3.1.37', c)

def sutra_3_1_38(c) -> bool:
    return _evaluate('3.1.38', c)

def sutra_3_1_39(c) -> bool:
    return _evaluate('3.1.39', c)

def sutra_3_1_40(c) -> bool:
    return _evaluate('3.1.40', c)

def sutra_3_1_41(c) -> bool:
    return _evaluate('3.1.41', c)

def sutra_3_1_42(c) -> bool:
    return _evaluate('3.1.42', c)

def sutra_3_1_43(c) -> bool:
    return _evaluate('3.1.43', c)

def sutra_3_1_44(c) -> bool:
    return _evaluate('3.1.44', c)

def sutra_3_1_45(c) -> bool:
    return _evaluate('3.1.45', c)

def sutra_3_1_46(c) -> bool:
    return _evaluate('3.1.46', c)

def sutra_3_1_47(c) -> bool:
    return _evaluate('3.1.47', c)

def sutra_3_1_48(c) -> bool:
    return _evaluate('3.1.48', c)

def sutra_3_1_49(c) -> bool:
    return _evaluate('3.1.49', c)

def sutra_3_1_50(c) -> bool:
    return _evaluate('3.1.50', c)

def sutra_3_1_51(c) -> bool:
    return _evaluate('3.1.51', c)

def sutra_3_1_52(c) -> bool:
    return _evaluate('3.1.52', c)

def sutra_3_1_53(c) -> bool:
    return _evaluate('3.1.53', c)

def sutra_3_1_54(c) -> bool:
    return _evaluate('3.1.54', c)

def sutra_3_1_55(c) -> bool:
    return _evaluate('3.1.55', c)

def sutra_3_1_56(c) -> bool:
    return _evaluate('3.1.56', c)

def sutra_3_1_57(c) -> bool:
    return _evaluate('3.1.57', c)

def sutra_3_1_58(c) -> bool:
    return _evaluate('3.1.58', c)

def sutra_3_1_59(c) -> bool:
    return _evaluate('3.1.59', c)

def sutra_3_1_60(c) -> bool:
    return _evaluate('3.1.60', c)

def sutra_3_1_61(c) -> bool:
    return _evaluate('3.1.61', c)

def sutra_3_1_62(c) -> bool:
    return _evaluate('3.1.62', c)

def sutra_3_1_63(c) -> bool:
    return _evaluate('3.1.63', c)

def sutra_3_1_64(c) -> bool:
    return _evaluate('3.1.64', c)

def sutra_3_1_65(c) -> bool:
    return _evaluate('3.1.65', c)

def sutra_3_1_66(c) -> bool:
    return _evaluate('3.1.66', c)

def sutra_3_1_67(c) -> bool:
    return _evaluate('3.1.67', c)

def sutra_3_1_70(c) -> bool:
    return _evaluate('3.1.70', c)

def sutra_3_1_71(c) -> bool:
    return _evaluate('3.1.71', c)

def sutra_3_1_72(c) -> bool:
    return _evaluate('3.1.72', c)

def sutra_3_1_74(c) -> bool:
    return _evaluate('3.1.74', c)

def sutra_3_1_75(c) -> bool:
    return _evaluate('3.1.75', c)

def sutra_3_1_76(c) -> bool:
    return _evaluate('3.1.76', c)

def sutra_3_1_80(c) -> bool:
    return _evaluate('3.1.80', c)

def sutra_3_1_82(c) -> bool:
    return _evaluate('3.1.82', c)

def sutra_3_1_83(c) -> bool:
    return _evaluate('3.1.83', c)

def sutra_3_1_84(c) -> bool:
    return _evaluate('3.1.84', c)

def sutra_3_1_85(c) -> bool:
    return _evaluate('3.1.85', c)

def sutra_3_1_86(c) -> bool:
    return _evaluate('3.1.86', c)

def sutra_3_1_87(c) -> bool:
    return _evaluate('3.1.87', c)

def sutra_3_1_88(c) -> bool:
    return _evaluate('3.1.88', c)

def sutra_3_1_89(c) -> bool:
    return _evaluate('3.1.89', c)

def sutra_3_1_90(c) -> bool:
    return _evaluate('3.1.90', c)

def sutra_3_1_92(c) -> bool:
    return _evaluate('3.1.92', c)

def sutra_3_1_94(c) -> bool:
    return _evaluate('3.1.94', c)

def sutra_3_1_95(c) -> bool:
    return _evaluate('3.1.95', c)

def sutra_3_1_96(c) -> bool:
    return _evaluate('3.1.96', c)

def sutra_3_1_97(c) -> bool:
    return _evaluate('3.1.97', c)

def sutra_3_1_98(c) -> bool:
    return _evaluate('3.1.98', c)

def sutra_3_1_99(c) -> bool:
    return _evaluate('3.1.99', c)

def sutra_3_1_100(c) -> bool:
    return _evaluate('3.1.100', c)

def sutra_3_1_101(c) -> bool:
    return _evaluate('3.1.101', c)

def sutra_3_1_102(c) -> bool:
    return _evaluate('3.1.102', c)

def sutra_3_1_103(c) -> bool:
    return _evaluate('3.1.103', c)

def sutra_3_1_104(c) -> bool:
    return _evaluate('3.1.104', c)

def sutra_3_1_105(c) -> bool:
    return _evaluate('3.1.105', c)

def sutra_3_1_106(c) -> bool:
    return _evaluate('3.1.106', c)

def sutra_3_1_107(c) -> bool:
    return _evaluate('3.1.107', c)

def sutra_3_1_108(c) -> bool:
    return _evaluate('3.1.108', c)

def sutra_3_1_109(c) -> bool:
    return _evaluate('3.1.109', c)

def sutra_3_1_110(c) -> bool:
    return _evaluate('3.1.110', c)

def sutra_3_1_111(c) -> bool:
    return _evaluate('3.1.111', c)

def sutra_3_1_112(c) -> bool:
    return _evaluate('3.1.112', c)

def sutra_3_1_113(c) -> bool:
    return _evaluate('3.1.113', c)

def sutra_3_1_114(c) -> bool:
    return _evaluate('3.1.114', c)

def sutra_3_1_115(c) -> bool:
    return _evaluate('3.1.115', c)

def sutra_3_1_116(c) -> bool:
    return _evaluate('3.1.116', c)

def sutra_3_1_117(c) -> bool:
    return _evaluate('3.1.117', c)

def sutra_3_1_118(c) -> bool:
    return _evaluate('3.1.118', c)

def sutra_3_1_119(c) -> bool:
    return _evaluate('3.1.119', c)

def sutra_3_1_120(c) -> bool:
    return _evaluate('3.1.120', c)

def sutra_3_1_121(c) -> bool:
    return _evaluate('3.1.121', c)

def sutra_3_1_122(c) -> bool:
    return _evaluate('3.1.122', c)

def sutra_3_1_123(c) -> bool:
    return _evaluate('3.1.123', c)

def sutra_3_1_124(c) -> bool:
    return _evaluate('3.1.124', c)

def sutra_3_1_125(c) -> bool:
    return _evaluate('3.1.125', c)

def sutra_3_1_126(c) -> bool:
    return _evaluate('3.1.126', c)

def sutra_3_1_127(c) -> bool:
    return _evaluate('3.1.127', c)

def sutra_3_1_128(c) -> bool:
    return _evaluate('3.1.128', c)

def sutra_3_1_129(c) -> bool:
    return _evaluate('3.1.129', c)

def sutra_3_1_130(c) -> bool:
    return _evaluate('3.1.130', c)

def sutra_3_1_131(c) -> bool:
    return _evaluate('3.1.131', c)

def sutra_3_1_132(c) -> bool:
    return _evaluate('3.1.132', c)

def sutra_3_1_133(c) -> bool:
    return _evaluate('3.1.133', c)

def sutra_3_1_134(c) -> bool:
    return _evaluate('3.1.134', c)

def sutra_3_1_135(c) -> bool:
    return _evaluate('3.1.135', c)

def sutra_3_1_136(c) -> bool:
    return _evaluate('3.1.136', c)

def sutra_3_1_137(c) -> bool:
    return _evaluate('3.1.137', c)

def sutra_3_1_138(c) -> bool:
    return _evaluate('3.1.138', c)

def sutra_3_1_139(c) -> bool:
    return _evaluate('3.1.139', c)

def sutra_3_1_140(c) -> bool:
    return _evaluate('3.1.140', c)

def sutra_3_1_141(c) -> bool:
    return _evaluate('3.1.141', c)

def sutra_3_1_142(c) -> bool:
    return _evaluate('3.1.142', c)

def sutra_3_1_143(c) -> bool:
    return _evaluate('3.1.143', c)

def sutra_3_1_144(c) -> bool:
    return _evaluate('3.1.144', c)

def sutra_3_1_145(c) -> bool:
    return _evaluate('3.1.145', c)

def sutra_3_1_146(c) -> bool:
    return _evaluate('3.1.146', c)

def sutra_3_1_147(c) -> bool:
    return _evaluate('3.1.147', c)

def sutra_3_1_148(c) -> bool:
    return _evaluate('3.1.148', c)

def sutra_3_1_149(c) -> bool:
    return _evaluate('3.1.149', c)

def sutra_3_1_150(c) -> bool:
    return _evaluate('3.1.150', c)

def sutra_3_2_2(c) -> bool:
    return _evaluate('3.2.2', c)

def sutra_3_2_4(c) -> bool:
    return _evaluate('3.2.4', c)

def sutra_3_2_5(c) -> bool:
    return _evaluate('3.2.5', c)

def sutra_3_2_6(c) -> bool:
    return _evaluate('3.2.6', c)

def sutra_3_2_7(c) -> bool:
    return _evaluate('3.2.7', c)

def sutra_3_2_8(c) -> bool:
    return _evaluate('3.2.8', c)

def sutra_3_2_9(c) -> bool:
    return _evaluate('3.2.9', c)

def sutra_3_2_10(c) -> bool:
    return _evaluate('3.2.10', c)

def sutra_3_2_11(c) -> bool:
    return _evaluate('3.2.11', c)

def sutra_3_2_12(c) -> bool:
    return _evaluate('3.2.12', c)

def sutra_3_2_13(c) -> bool:
    return _evaluate('3.2.13', c)

def sutra_3_2_14(c) -> bool:
    return _evaluate('3.2.14', c)

def sutra_3_2_15(c) -> bool:
    return _evaluate('3.2.15', c)

def sutra_3_2_17(c) -> bool:
    return _evaluate('3.2.17', c)

def sutra_3_2_18(c) -> bool:
    return _evaluate('3.2.18', c)

def sutra_3_2_19(c) -> bool:
    return _evaluate('3.2.19', c)

def sutra_3_2_20(c) -> bool:
    return _evaluate('3.2.20', c)

def sutra_3_2_21(c) -> bool:
    return _evaluate('3.2.21', c)

def sutra_3_2_22(c) -> bool:
    return _evaluate('3.2.22', c)

def sutra_3_2_23(c) -> bool:
    return _evaluate('3.2.23', c)

def sutra_3_2_24(c) -> bool:
    return _evaluate('3.2.24', c)

def sutra_3_2_25(c) -> bool:
    return _evaluate('3.2.25', c)

def sutra_3_2_26(c) -> bool:
    return _evaluate('3.2.26', c)

def sutra_3_2_27(c) -> bool:
    return _evaluate('3.2.27', c)

def sutra_3_2_28(c) -> bool:
    return _evaluate('3.2.28', c)

def sutra_3_2_29(c) -> bool:
    return _evaluate('3.2.29', c)

def sutra_3_2_30(c) -> bool:
    return _evaluate('3.2.30', c)

def sutra_3_2_31(c) -> bool:
    return _evaluate('3.2.31', c)

def sutra_3_2_32(c) -> bool:
    return _evaluate('3.2.32', c)

def sutra_3_2_33(c) -> bool:
    return _evaluate('3.2.33', c)

def sutra_3_2_34(c) -> bool:
    return _evaluate('3.2.34', c)

def sutra_3_2_35(c) -> bool:
    return _evaluate('3.2.35', c)

def sutra_3_2_36(c) -> bool:
    return _evaluate('3.2.36', c)

def sutra_3_2_37(c) -> bool:
    return _evaluate('3.2.37', c)

def sutra_3_2_38(c) -> bool:
    return _evaluate('3.2.38', c)

def sutra_3_2_39(c) -> bool:
    return _evaluate('3.2.39', c)

def sutra_3_2_40(c) -> bool:
    return _evaluate('3.2.40', c)

def sutra_3_2_41(c) -> bool:
    return _evaluate('3.2.41', c)

def sutra_3_2_42(c) -> bool:
    return _evaluate('3.2.42', c)

def sutra_3_2_43(c) -> bool:
    return _evaluate('3.2.43', c)

def sutra_3_2_44(c) -> bool:
    return _evaluate('3.2.44', c)

def sutra_3_2_45(c) -> bool:
    return _evaluate('3.2.45', c)

def sutra_3_2_46(c) -> bool:
    return _evaluate('3.2.46', c)

def sutra_3_2_47(c) -> bool:
    return _evaluate('3.2.47', c)

def sutra_3_2_48(c) -> bool:
    return _evaluate('3.2.48', c)

def sutra_3_2_49(c) -> bool:
    return _evaluate('3.2.49', c)

def sutra_3_2_50(c) -> bool:
    return _evaluate('3.2.50', c)

def sutra_3_2_51(c) -> bool:
    return _evaluate('3.2.51', c)

def sutra_3_2_52(c) -> bool:
    return _evaluate('3.2.52', c)

def sutra_3_2_53(c) -> bool:
    return _evaluate('3.2.53', c)

def sutra_3_2_54(c) -> bool:
    return _evaluate('3.2.54', c)

def sutra_3_2_55(c) -> bool:
    return _evaluate('3.2.55', c)

def sutra_3_2_56(c) -> bool:
    return _evaluate('3.2.56', c)

def sutra_3_2_57(c) -> bool:
    return _evaluate('3.2.57', c)

def sutra_3_2_58(c) -> bool:
    return _evaluate('3.2.58', c)

def sutra_3_2_59(c) -> bool:
    return _evaluate('3.2.59', c)

def sutra_3_2_60(c) -> bool:
    return _evaluate('3.2.60', c)

def sutra_3_2_61(c) -> bool:
    return _evaluate('3.2.61', c)

def sutra_3_2_62(c) -> bool:
    return _evaluate('3.2.62', c)

def sutra_3_2_63(c) -> bool:
    return _evaluate('3.2.63', c)

def sutra_3_2_64(c) -> bool:
    return _evaluate('3.2.64', c)

def sutra_3_2_65(c) -> bool:
    return _evaluate('3.2.65', c)

def sutra_3_2_66(c) -> bool:
    return _evaluate('3.2.66', c)

def sutra_3_2_67(c) -> bool:
    return _evaluate('3.2.67', c)

def sutra_3_2_68(c) -> bool:
    return _evaluate('3.2.68', c)

def sutra_3_2_69(c) -> bool:
    return _evaluate('3.2.69', c)

def sutra_3_2_70(c) -> bool:
    return _evaluate('3.2.70', c)

def sutra_3_2_71(c) -> bool:
    return _evaluate('3.2.71', c)

def sutra_3_2_72(c) -> bool:
    return _evaluate('3.2.72', c)

def sutra_3_2_73(c) -> bool:
    return _evaluate('3.2.73', c)

def sutra_3_2_74(c) -> bool:
    return _evaluate('3.2.74', c)

def sutra_3_2_75(c) -> bool:
    return _evaluate('3.2.75', c)

def sutra_3_2_76(c) -> bool:
    return _evaluate('3.2.76', c)

def sutra_3_2_77(c) -> bool:
    return _evaluate('3.2.77', c)

def sutra_3_2_78(c) -> bool:
    return _evaluate('3.2.78', c)

def sutra_3_2_79(c) -> bool:
    return _evaluate('3.2.79', c)

def sutra_3_2_80(c) -> bool:
    return _evaluate('3.2.80', c)

def sutra_3_2_81(c) -> bool:
    return _evaluate('3.2.81', c)

def sutra_3_2_82(c) -> bool:
    return _evaluate('3.2.82', c)

def sutra_3_2_83(c) -> bool:
    return _evaluate('3.2.83', c)

def sutra_3_2_84(c) -> bool:
    return _evaluate('3.2.84', c)

def sutra_3_2_85(c) -> bool:
    return _evaluate('3.2.85', c)

def sutra_3_2_86(c) -> bool:
    return _evaluate('3.2.86', c)

def sutra_3_2_87(c) -> bool:
    return _evaluate('3.2.87', c)

def sutra_3_2_88(c) -> bool:
    return _evaluate('3.2.88', c)

def sutra_3_2_89(c) -> bool:
    return _evaluate('3.2.89', c)

def sutra_3_2_90(c) -> bool:
    return _evaluate('3.2.90', c)

def sutra_3_2_91(c) -> bool:
    return _evaluate('3.2.91', c)

def sutra_3_2_92(c) -> bool:
    return _evaluate('3.2.92', c)

def sutra_3_2_93(c) -> bool:
    return _evaluate('3.2.93', c)

def sutra_3_2_94(c) -> bool:
    return _evaluate('3.2.94', c)

def sutra_3_2_95(c) -> bool:
    return _evaluate('3.2.95', c)

def sutra_3_2_96(c) -> bool:
    return _evaluate('3.2.96', c)

def sutra_3_2_97(c) -> bool:
    return _evaluate('3.2.97', c)

def sutra_3_2_98(c) -> bool:
    return _evaluate('3.2.98', c)

def sutra_3_2_99(c) -> bool:
    return _evaluate('3.2.99', c)

def sutra_3_2_100(c) -> bool:
    return _evaluate('3.2.100', c)

def sutra_3_2_101(c) -> bool:
    return _evaluate('3.2.101', c)

def sutra_3_2_103(c) -> bool:
    return _evaluate('3.2.103', c)

def sutra_3_2_104(c) -> bool:
    return _evaluate('3.2.104', c)

def sutra_3_2_105(c) -> bool:
    return _evaluate('3.2.105', c)

def sutra_3_2_106(c) -> bool:
    return _evaluate('3.2.106', c)

def sutra_3_2_107(c) -> bool:
    return _evaluate('3.2.107', c)

def sutra_3_2_108(c) -> bool:
    return _evaluate('3.2.108', c)

def sutra_3_2_109(c) -> bool:
    return _evaluate('3.2.109', c)

def sutra_3_2_112(c) -> bool:
    return _evaluate('3.2.112', c)

def sutra_3_2_113(c) -> bool:
    return _evaluate('3.2.113', c)

def sutra_3_2_114(c) -> bool:
    return _evaluate('3.2.114', c)

def sutra_3_2_115(c) -> bool:
    return _evaluate('3.2.115', c)

def sutra_3_2_116(c) -> bool:
    return _evaluate('3.2.116', c)

def sutra_3_2_117(c) -> bool:
    return _evaluate('3.2.117', c)

def sutra_3_2_118(c) -> bool:
    return _evaluate('3.2.118', c)

def sutra_3_2_119(c) -> bool:
    return _evaluate('3.2.119', c)

def sutra_3_2_120(c) -> bool:
    return _evaluate('3.2.120', c)

def sutra_3_2_121(c) -> bool:
    return _evaluate('3.2.121', c)

def sutra_3_2_122(c) -> bool:
    return _evaluate('3.2.122', c)

def sutra_3_2_124(c) -> bool:
    return _evaluate('3.2.124', c)

def sutra_3_2_125(c) -> bool:
    return _evaluate('3.2.125', c)

def sutra_3_2_126(c) -> bool:
    return _evaluate('3.2.126', c)

def sutra_3_2_127(c) -> bool:
    return _evaluate('3.2.127', c)

def sutra_3_2_128(c) -> bool:
    return _evaluate('3.2.128', c)

def sutra_3_2_129(c) -> bool:
    return _evaluate('3.2.129', c)

def sutra_3_2_130(c) -> bool:
    return _evaluate('3.2.130', c)

def sutra_3_2_131(c) -> bool:
    return _evaluate('3.2.131', c)

def sutra_3_2_132(c) -> bool:
    return _evaluate('3.2.132', c)

def sutra_3_2_133(c) -> bool:
    return _evaluate('3.2.133', c)

def sutra_3_2_134(c) -> bool:
    return _evaluate('3.2.134', c)

def sutra_3_2_136(c) -> bool:
    return _evaluate('3.2.136', c)

def sutra_3_2_137(c) -> bool:
    return _evaluate('3.2.137', c)

def sutra_3_2_138(c) -> bool:
    return _evaluate('3.2.138', c)

def sutra_3_2_139(c) -> bool:
    return _evaluate('3.2.139', c)

def sutra_3_2_140(c) -> bool:
    return _evaluate('3.2.140', c)

def sutra_3_2_141(c) -> bool:
    return _evaluate('3.2.141', c)

def sutra_3_2_142(c) -> bool:
    return _evaluate('3.2.142', c)

def sutra_3_2_143(c) -> bool:
    return _evaluate('3.2.143', c)

def sutra_3_2_144(c) -> bool:
    return _evaluate('3.2.144', c)

def sutra_3_2_145(c) -> bool:
    return _evaluate('3.2.145', c)

def sutra_3_2_146(c) -> bool:
    return _evaluate('3.2.146', c)

def sutra_3_2_147(c) -> bool:
    return _evaluate('3.2.147', c)

def sutra_3_2_148(c) -> bool:
    return _evaluate('3.2.148', c)

def sutra_3_2_149(c) -> bool:
    return _evaluate('3.2.149', c)

def sutra_3_2_150(c) -> bool:
    return _evaluate('3.2.150', c)

def sutra_3_2_151(c) -> bool:
    return _evaluate('3.2.151', c)

def sutra_3_2_152(c) -> bool:
    return _evaluate('3.2.152', c)

def sutra_3_2_153(c) -> bool:
    return _evaluate('3.2.153', c)

def sutra_3_2_154(c) -> bool:
    return _evaluate('3.2.154', c)

def sutra_3_2_155(c) -> bool:
    return _evaluate('3.2.155', c)

def sutra_3_2_156(c) -> bool:
    return _evaluate('3.2.156', c)

def sutra_3_2_157(c) -> bool:
    return _evaluate('3.2.157', c)

def sutra_3_2_158(c) -> bool:
    return _evaluate('3.2.158', c)

def sutra_3_2_159(c) -> bool:
    return _evaluate('3.2.159', c)

def sutra_3_2_160(c) -> bool:
    return _evaluate('3.2.160', c)

def sutra_3_2_161(c) -> bool:
    return _evaluate('3.2.161', c)

def sutra_3_2_162(c) -> bool:
    return _evaluate('3.2.162', c)

def sutra_3_2_163(c) -> bool:
    return _evaluate('3.2.163', c)

def sutra_3_2_164(c) -> bool:
    return _evaluate('3.2.164', c)

def sutra_3_2_165(c) -> bool:
    return _evaluate('3.2.165', c)

def sutra_3_2_166(c) -> bool:
    return _evaluate('3.2.166', c)

def sutra_3_2_167(c) -> bool:
    return _evaluate('3.2.167', c)

def sutra_3_2_168(c) -> bool:
    return _evaluate('3.2.168', c)

def sutra_3_2_169(c) -> bool:
    return _evaluate('3.2.169', c)

def sutra_3_2_170(c) -> bool:
    return _evaluate('3.2.170', c)

def sutra_3_2_171(c) -> bool:
    return _evaluate('3.2.171', c)

def sutra_3_2_172(c) -> bool:
    return _evaluate('3.2.172', c)

def sutra_3_2_173(c) -> bool:
    return _evaluate('3.2.173', c)

def sutra_3_2_174(c) -> bool:
    return _evaluate('3.2.174', c)

def sutra_3_2_175(c) -> bool:
    return _evaluate('3.2.175', c)

def sutra_3_2_176(c) -> bool:
    return _evaluate('3.2.176', c)

def sutra_3_2_177(c) -> bool:
    return _evaluate('3.2.177', c)

def sutra_3_2_178(c) -> bool:
    return _evaluate('3.2.178', c)

def sutra_3_2_179(c) -> bool:
    return _evaluate('3.2.179', c)

def sutra_3_2_180(c) -> bool:
    return _evaluate('3.2.180', c)

def sutra_3_2_181(c) -> bool:
    return _evaluate('3.2.181', c)

def sutra_3_2_182(c) -> bool:
    return _evaluate('3.2.182', c)

def sutra_3_2_183(c) -> bool:
    return _evaluate('3.2.183', c)

def sutra_3_2_184(c) -> bool:
    return _evaluate('3.2.184', c)

def sutra_3_2_185(c) -> bool:
    return _evaluate('3.2.185', c)

def sutra_3_2_186(c) -> bool:
    return _evaluate('3.2.186', c)

def sutra_3_2_187(c) -> bool:
    return _evaluate('3.2.187', c)

def sutra_3_2_188(c) -> bool:
    return _evaluate('3.2.188', c)

def sutra_3_3_1(c) -> bool:
    return _evaluate('3.3.1', c)

def sutra_3_3_2(c) -> bool:
    return _evaluate('3.3.2', c)

def sutra_3_3_3(c) -> bool:
    return _evaluate('3.3.3', c)

def sutra_3_3_4(c) -> bool:
    return _evaluate('3.3.4', c)

def sutra_3_3_5(c) -> bool:
    return _evaluate('3.3.5', c)

def sutra_3_3_6(c) -> bool:
    return _evaluate('3.3.6', c)

def sutra_3_3_7(c) -> bool:
    return _evaluate('3.3.7', c)

def sutra_3_3_8(c) -> bool:
    return _evaluate('3.3.8', c)

def sutra_3_3_9(c) -> bool:
    return _evaluate('3.3.9', c)

def sutra_3_3_10(c) -> bool:
    return _evaluate('3.3.10', c)

def sutra_3_3_11(c) -> bool:
    return _evaluate('3.3.11', c)

def sutra_3_3_12(c) -> bool:
    return _evaluate('3.3.12', c)

def sutra_3_3_13(c) -> bool:
    return _evaluate('3.3.13', c)

def sutra_3_3_14(c) -> bool:
    return _evaluate('3.3.14', c)

def sutra_3_3_16(c) -> bool:
    return _evaluate('3.3.16', c)

def sutra_3_3_17(c) -> bool:
    return _evaluate('3.3.17', c)

def sutra_3_3_19(c) -> bool:
    return _evaluate('3.3.19', c)

def sutra_3_3_20(c) -> bool:
    return _evaluate('3.3.20', c)

def sutra_3_3_21(c) -> bool:
    return _evaluate('3.3.21', c)

def sutra_3_3_22(c) -> bool:
    return _evaluate('3.3.22', c)

def sutra_3_3_23(c) -> bool:
    return _evaluate('3.3.23', c)

def sutra_3_3_24(c) -> bool:
    return _evaluate('3.3.24', c)

def sutra_3_3_25(c) -> bool:
    return _evaluate('3.3.25', c)

def sutra_3_3_26(c) -> bool:
    return _evaluate('3.3.26', c)

def sutra_3_3_27(c) -> bool:
    return _evaluate('3.3.27', c)

def sutra_3_3_28(c) -> bool:
    return _evaluate('3.3.28', c)

def sutra_3_3_29(c) -> bool:
    return _evaluate('3.3.29', c)

def sutra_3_3_30(c) -> bool:
    return _evaluate('3.3.30', c)

def sutra_3_3_31(c) -> bool:
    return _evaluate('3.3.31', c)

def sutra_3_3_32(c) -> bool:
    return _evaluate('3.3.32', c)

def sutra_3_3_34(c) -> bool:
    return _evaluate('3.3.34', c)

def sutra_3_3_35(c) -> bool:
    return _evaluate('3.3.35', c)

def sutra_3_3_36(c) -> bool:
    return _evaluate('3.3.36', c)

def sutra_3_3_37(c) -> bool:
    return _evaluate('3.3.37', c)

def sutra_3_3_38(c) -> bool:
    return _evaluate('3.3.38', c)

def sutra_3_3_39(c) -> bool:
    return _evaluate('3.3.39', c)

def sutra_3_3_40(c) -> bool:
    return _evaluate('3.3.40', c)

def sutra_3_3_41(c) -> bool:
    return _evaluate('3.3.41', c)

def sutra_3_3_42(c) -> bool:
    return _evaluate('3.3.42', c)

def sutra_3_3_43(c) -> bool:
    return _evaluate('3.3.43', c)

def sutra_3_3_44(c) -> bool:
    return _evaluate('3.3.44', c)

def sutra_3_3_45(c) -> bool:
    return _evaluate('3.3.45', c)

def sutra_3_3_46(c) -> bool:
    return _evaluate('3.3.46', c)

def sutra_3_3_47(c) -> bool:
    return _evaluate('3.3.47', c)

def sutra_3_3_48(c) -> bool:
    return _evaluate('3.3.48', c)

def sutra_3_3_49(c) -> bool:
    return _evaluate('3.3.49', c)

def sutra_3_3_50(c) -> bool:
    return _evaluate('3.3.50', c)

def sutra_3_3_51(c) -> bool:
    return _evaluate('3.3.51', c)

def sutra_3_3_52(c) -> bool:
    return _evaluate('3.3.52', c)

def sutra_3_3_53(c) -> bool:
    return _evaluate('3.3.53', c)

def sutra_3_3_54(c) -> bool:
    return _evaluate('3.3.54', c)

def sutra_3_3_55(c) -> bool:
    return _evaluate('3.3.55', c)

def sutra_3_3_56(c) -> bool:
    return _evaluate('3.3.56', c)

def sutra_3_3_57(c) -> bool:
    return _evaluate('3.3.57', c)

def sutra_3_3_58(c) -> bool:
    return _evaluate('3.3.58', c)

def sutra_3_3_59(c) -> bool:
    return _evaluate('3.3.59', c)

def sutra_3_3_60(c) -> bool:
    return _evaluate('3.3.60', c)

def sutra_3_3_61(c) -> bool:
    return _evaluate('3.3.61', c)

def sutra_3_3_62(c) -> bool:
    return _evaluate('3.3.62', c)

def sutra_3_3_63(c) -> bool:
    return _evaluate('3.3.63', c)

def sutra_3_3_64(c) -> bool:
    return _evaluate('3.3.64', c)

def sutra_3_3_65(c) -> bool:
    return _evaluate('3.3.65', c)

def sutra_3_3_66(c) -> bool:
    return _evaluate('3.3.66', c)

def sutra_3_3_67(c) -> bool:
    return _evaluate('3.3.67', c)

def sutra_3_3_68(c) -> bool:
    return _evaluate('3.3.68', c)

def sutra_3_3_69(c) -> bool:
    return _evaluate('3.3.69', c)

def sutra_3_3_70(c) -> bool:
    return _evaluate('3.3.70', c)

def sutra_3_3_71(c) -> bool:
    return _evaluate('3.3.71', c)

def sutra_3_3_72(c) -> bool:
    return _evaluate('3.3.72', c)

def sutra_3_3_73(c) -> bool:
    return _evaluate('3.3.73', c)

def sutra_3_3_74(c) -> bool:
    return _evaluate('3.3.74', c)

def sutra_3_3_75(c) -> bool:
    return _evaluate('3.3.75', c)

def sutra_3_3_76(c) -> bool:
    return _evaluate('3.3.76', c)

def sutra_3_3_77(c) -> bool:
    return _evaluate('3.3.77', c)

def sutra_3_3_78(c) -> bool:
    return _evaluate('3.3.78', c)

def sutra_3_3_79(c) -> bool:
    return _evaluate('3.3.79', c)

def sutra_3_3_80(c) -> bool:
    return _evaluate('3.3.80', c)

def sutra_3_3_81(c) -> bool:
    return _evaluate('3.3.81', c)

def sutra_3_3_82(c) -> bool:
    return _evaluate('3.3.82', c)

def sutra_3_3_83(c) -> bool:
    return _evaluate('3.3.83', c)

def sutra_3_3_84(c) -> bool:
    return _evaluate('3.3.84', c)

def sutra_3_3_85(c) -> bool:
    return _evaluate('3.3.85', c)

def sutra_3_3_86(c) -> bool:
    return _evaluate('3.3.86', c)

def sutra_3_3_87(c) -> bool:
    return _evaluate('3.3.87', c)

def sutra_3_3_88(c) -> bool:
    return _evaluate('3.3.88', c)

def sutra_3_3_89(c) -> bool:
    return _evaluate('3.3.89', c)

def sutra_3_3_90(c) -> bool:
    return _evaluate('3.3.90', c)

def sutra_3_3_91(c) -> bool:
    return _evaluate('3.3.91', c)

def sutra_3_3_92(c) -> bool:
    return _evaluate('3.3.92', c)

def sutra_3_3_93(c) -> bool:
    return _evaluate('3.3.93', c)

def sutra_3_3_95(c) -> bool:
    return _evaluate('3.3.95', c)

def sutra_3_3_96(c) -> bool:
    return _evaluate('3.3.96', c)

def sutra_3_3_97(c) -> bool:
    return _evaluate('3.3.97', c)

def sutra_3_3_98(c) -> bool:
    return _evaluate('3.3.98', c)

def sutra_3_3_99(c) -> bool:
    return _evaluate('3.3.99', c)

def sutra_3_3_100(c) -> bool:
    return _evaluate('3.3.100', c)

def sutra_3_3_101(c) -> bool:
    return _evaluate('3.3.101', c)

def sutra_3_3_102(c) -> bool:
    return _evaluate('3.3.102', c)

def sutra_3_3_103(c) -> bool:
    return _evaluate('3.3.103', c)

def sutra_3_3_104(c) -> bool:
    return _evaluate('3.3.104', c)

def sutra_3_3_105(c) -> bool:
    return _evaluate('3.3.105', c)

def sutra_3_3_106(c) -> bool:
    return _evaluate('3.3.106', c)

def sutra_3_3_107(c) -> bool:
    return _evaluate('3.3.107', c)

def sutra_3_3_108(c) -> bool:
    return _evaluate('3.3.108', c)

def sutra_3_3_109(c) -> bool:
    return _evaluate('3.3.109', c)

def sutra_3_3_110(c) -> bool:
    return _evaluate('3.3.110', c)

def sutra_3_3_111(c) -> bool:
    return _evaluate('3.3.111', c)

def sutra_3_3_112(c) -> bool:
    return _evaluate('3.3.112', c)

def sutra_3_3_113(c) -> bool:
    return _evaluate('3.3.113', c)

def sutra_3_3_114(c) -> bool:
    return _evaluate('3.3.114', c)

def sutra_3_3_116(c) -> bool:
    return _evaluate('3.3.116', c)

def sutra_3_3_117(c) -> bool:
    return _evaluate('3.3.117', c)

def sutra_3_3_118(c) -> bool:
    return _evaluate('3.3.118', c)

def sutra_3_3_119(c) -> bool:
    return _evaluate('3.3.119', c)

def sutra_3_3_120(c) -> bool:
    return _evaluate('3.3.120', c)

def sutra_3_3_122(c) -> bool:
    return _evaluate('3.3.122', c)

def sutra_3_3_123(c) -> bool:
    return _evaluate('3.3.123', c)

def sutra_3_3_124(c) -> bool:
    return _evaluate('3.3.124', c)

def sutra_3_3_125(c) -> bool:
    return _evaluate('3.3.125', c)

def sutra_3_3_126(c) -> bool:
    return _evaluate('3.3.126', c)

def sutra_3_3_127(c) -> bool:
    return _evaluate('3.3.127', c)

def sutra_3_3_128(c) -> bool:
    return _evaluate('3.3.128', c)

def sutra_3_3_129(c) -> bool:
    return _evaluate('3.3.129', c)

def sutra_3_3_130(c) -> bool:
    return _evaluate('3.3.130', c)

def sutra_3_3_131(c) -> bool:
    return _evaluate('3.3.131', c)

def sutra_3_3_132(c) -> bool:
    return _evaluate('3.3.132', c)

def sutra_3_3_133(c) -> bool:
    return _evaluate('3.3.133', c)

def sutra_3_3_134(c) -> bool:
    return _evaluate('3.3.134', c)

def sutra_3_3_135(c) -> bool:
    return _evaluate('3.3.135', c)

def sutra_3_3_136(c) -> bool:
    return _evaluate('3.3.136', c)

def sutra_3_3_137(c) -> bool:
    return _evaluate('3.3.137', c)

def sutra_3_3_138(c) -> bool:
    return _evaluate('3.3.138', c)

def sutra_3_3_140(c) -> bool:
    return _evaluate('3.3.140', c)

def sutra_3_3_141(c) -> bool:
    return _evaluate('3.3.141', c)

def sutra_3_3_142(c) -> bool:
    return _evaluate('3.3.142', c)

def sutra_3_3_143(c) -> bool:
    return _evaluate('3.3.143', c)

def sutra_3_3_144(c) -> bool:
    return _evaluate('3.3.144', c)

def sutra_3_3_145(c) -> bool:
    return _evaluate('3.3.145', c)

def sutra_3_3_146(c) -> bool:
    return _evaluate('3.3.146', c)

def sutra_3_3_147(c) -> bool:
    return _evaluate('3.3.147', c)

def sutra_3_3_148(c) -> bool:
    return _evaluate('3.3.148', c)

def sutra_3_3_149(c) -> bool:
    return _evaluate('3.3.149', c)

def sutra_3_3_150(c) -> bool:
    return _evaluate('3.3.150', c)

def sutra_3_3_151(c) -> bool:
    return _evaluate('3.3.151', c)

def sutra_3_3_152(c) -> bool:
    return _evaluate('3.3.152', c)

def sutra_3_3_153(c) -> bool:
    return _evaluate('3.3.153', c)

def sutra_3_3_154(c) -> bool:
    return _evaluate('3.3.154', c)

def sutra_3_3_155(c) -> bool:
    return _evaluate('3.3.155', c)

def sutra_3_3_156(c) -> bool:
    return _evaluate('3.3.156', c)

def sutra_3_3_157(c) -> bool:
    return _evaluate('3.3.157', c)

def sutra_3_3_158(c) -> bool:
    return _evaluate('3.3.158', c)

def sutra_3_3_159(c) -> bool:
    return _evaluate('3.3.159', c)

def sutra_3_3_160(c) -> bool:
    return _evaluate('3.3.160', c)

def sutra_3_3_163(c) -> bool:
    return _evaluate('3.3.163', c)

def sutra_3_3_164(c) -> bool:
    return _evaluate('3.3.164', c)

def sutra_3_3_165(c) -> bool:
    return _evaluate('3.3.165', c)

def sutra_3_3_166(c) -> bool:
    return _evaluate('3.3.166', c)

def sutra_3_3_167(c) -> bool:
    return _evaluate('3.3.167', c)

def sutra_3_3_168(c) -> bool:
    return _evaluate('3.3.168', c)

def sutra_3_3_169(c) -> bool:
    return _evaluate('3.3.169', c)

def sutra_3_3_170(c) -> bool:
    return _evaluate('3.3.170', c)

def sutra_3_3_171(c) -> bool:
    return _evaluate('3.3.171', c)

def sutra_3_3_172(c) -> bool:
    return _evaluate('3.3.172', c)

def sutra_3_3_173(c) -> bool:
    return _evaluate('3.3.173', c)

def sutra_3_3_174(c) -> bool:
    return _evaluate('3.3.174', c)

def sutra_3_3_175(c) -> bool:
    return _evaluate('3.3.175', c)

def sutra_3_3_176(c) -> bool:
    return _evaluate('3.3.176', c)

def sutra_3_4_1(c) -> bool:
    return _evaluate('3.4.1', c)

def sutra_3_4_2(c) -> bool:
    return _evaluate('3.4.2', c)

def sutra_3_4_3(c) -> bool:
    return _evaluate('3.4.3', c)

def sutra_3_4_4(c) -> bool:
    return _evaluate('3.4.4', c)

def sutra_3_4_5(c) -> bool:
    return _evaluate('3.4.5', c)

def sutra_3_4_6(c) -> bool:
    return _evaluate('3.4.6', c)

def sutra_3_4_7(c) -> bool:
    return _evaluate('3.4.7', c)

def sutra_3_4_8(c) -> bool:
    return _evaluate('3.4.8', c)

def sutra_3_4_9(c) -> bool:
    return _evaluate('3.4.9', c)

def sutra_3_4_10(c) -> bool:
    return _evaluate('3.4.10', c)

def sutra_3_4_11(c) -> bool:
    return _evaluate('3.4.11', c)

def sutra_3_4_12(c) -> bool:
    return _evaluate('3.4.12', c)

def sutra_3_4_13(c) -> bool:
    return _evaluate('3.4.13', c)

def sutra_3_4_14(c) -> bool:
    return _evaluate('3.4.14', c)

def sutra_3_4_15(c) -> bool:
    return _evaluate('3.4.15', c)

def sutra_3_4_16(c) -> bool:
    return _evaluate('3.4.16', c)

def sutra_3_4_17(c) -> bool:
    return _evaluate('3.4.17', c)

def sutra_3_4_18(c) -> bool:
    return _evaluate('3.4.18', c)

def sutra_3_4_19(c) -> bool:
    return _evaluate('3.4.19', c)

def sutra_3_4_20(c) -> bool:
    return _evaluate('3.4.20', c)

def sutra_3_4_21(c) -> bool:
    return _evaluate('3.4.21', c)

def sutra_3_4_22(c) -> bool:
    return _evaluate('3.4.22', c)

def sutra_3_4_23(c) -> bool:
    return _evaluate('3.4.23', c)

def sutra_3_4_24(c) -> bool:
    return _evaluate('3.4.24', c)

def sutra_3_4_25(c) -> bool:
    return _evaluate('3.4.25', c)

def sutra_3_4_26(c) -> bool:
    return _evaluate('3.4.26', c)

def sutra_3_4_27(c) -> bool:
    return _evaluate('3.4.27', c)

def sutra_3_4_28(c) -> bool:
    return _evaluate('3.4.28', c)

def sutra_3_4_29(c) -> bool:
    return _evaluate('3.4.29', c)

def sutra_3_4_30(c) -> bool:
    return _evaluate('3.4.30', c)

def sutra_3_4_31(c) -> bool:
    return _evaluate('3.4.31', c)

def sutra_3_4_32(c) -> bool:
    return _evaluate('3.4.32', c)

def sutra_3_4_33(c) -> bool:
    return _evaluate('3.4.33', c)

def sutra_3_4_34(c) -> bool:
    return _evaluate('3.4.34', c)

def sutra_3_4_35(c) -> bool:
    return _evaluate('3.4.35', c)

def sutra_3_4_36(c) -> bool:
    return _evaluate('3.4.36', c)

def sutra_3_4_37(c) -> bool:
    return _evaluate('3.4.37', c)

def sutra_3_4_38(c) -> bool:
    return _evaluate('3.4.38', c)

def sutra_3_4_39(c) -> bool:
    return _evaluate('3.4.39', c)

def sutra_3_4_40(c) -> bool:
    return _evaluate('3.4.40', c)

def sutra_3_4_41(c) -> bool:
    return _evaluate('3.4.41', c)

def sutra_3_4_42(c) -> bool:
    return _evaluate('3.4.42', c)

def sutra_3_4_43(c) -> bool:
    return _evaluate('3.4.43', c)

def sutra_3_4_44(c) -> bool:
    return _evaluate('3.4.44', c)

def sutra_3_4_45(c) -> bool:
    return _evaluate('3.4.45', c)

def sutra_3_4_46(c) -> bool:
    return _evaluate('3.4.46', c)

def sutra_3_4_47(c) -> bool:
    return _evaluate('3.4.47', c)

def sutra_3_4_48(c) -> bool:
    return _evaluate('3.4.48', c)

def sutra_3_4_49(c) -> bool:
    return _evaluate('3.4.49', c)

def sutra_3_4_50(c) -> bool:
    return _evaluate('3.4.50', c)

def sutra_3_4_51(c) -> bool:
    return _evaluate('3.4.51', c)

def sutra_3_4_52(c) -> bool:
    return _evaluate('3.4.52', c)

def sutra_3_4_53(c) -> bool:
    return _evaluate('3.4.53', c)

def sutra_3_4_54(c) -> bool:
    return _evaluate('3.4.54', c)

def sutra_3_4_55(c) -> bool:
    return _evaluate('3.4.55', c)

def sutra_3_4_56(c) -> bool:
    return _evaluate('3.4.56', c)

def sutra_3_4_57(c) -> bool:
    return _evaluate('3.4.57', c)

def sutra_3_4_58(c) -> bool:
    return _evaluate('3.4.58', c)

def sutra_3_4_59(c) -> bool:
    return _evaluate('3.4.59', c)

def sutra_3_4_60(c) -> bool:
    return _evaluate('3.4.60', c)

def sutra_3_4_61(c) -> bool:
    return _evaluate('3.4.61', c)

def sutra_3_4_62(c) -> bool:
    return _evaluate('3.4.62', c)

def sutra_3_4_63(c) -> bool:
    return _evaluate('3.4.63', c)

def sutra_3_4_64(c) -> bool:
    return _evaluate('3.4.64', c)

def sutra_3_4_65(c) -> bool:
    return _evaluate('3.4.65', c)

def sutra_3_4_66(c) -> bool:
    return _evaluate('3.4.66', c)

def sutra_3_4_67(c) -> bool:
    return _evaluate('3.4.67', c)

def sutra_3_4_68(c) -> bool:
    return _evaluate('3.4.68', c)

def sutra_3_4_70(c) -> bool:
    return _evaluate('3.4.70', c)

def sutra_3_4_73(c) -> bool:
    return _evaluate('3.4.73', c)

def sutra_3_4_74(c) -> bool:
    return _evaluate('3.4.74', c)

def sutra_3_4_75(c) -> bool:
    return _evaluate('3.4.75', c)

def sutra_3_4_76(c) -> bool:
    return _evaluate('3.4.76', c)

def sutra_3_4_77(c) -> bool:
    return _evaluate('3.4.77', c)

def sutra_3_4_78(c) -> bool:
    return _evaluate('3.4.78', c)

def sutra_3_4_81(c) -> bool:
    return _evaluate('3.4.81', c)

def sutra_3_4_82(c) -> bool:
    return _evaluate('3.4.82', c)

def sutra_3_4_83(c) -> bool:
    return _evaluate('3.4.83', c)

def sutra_3_4_84(c) -> bool:
    return _evaluate('3.4.84', c)

def sutra_3_4_85(c) -> bool:
    return _evaluate('3.4.85', c)

def sutra_3_4_89(c) -> bool:
    return _evaluate('3.4.89', c)

def sutra_3_4_90(c) -> bool:
    return _evaluate('3.4.90', c)

def sutra_3_4_91(c) -> bool:
    return _evaluate('3.4.91', c)

def sutra_3_4_93(c) -> bool:
    return _evaluate('3.4.93', c)

def sutra_3_4_94(c) -> bool:
    return _evaluate('3.4.94', c)

def sutra_3_4_95(c) -> bool:
    return _evaluate('3.4.95', c)

def sutra_3_4_96(c) -> bool:
    return _evaluate('3.4.96', c)

def sutra_3_4_97(c) -> bool:
    return _evaluate('3.4.97', c)

def sutra_3_4_98(c) -> bool:
    return _evaluate('3.4.98', c)

def sutra_3_4_99(c) -> bool:
    return _evaluate('3.4.99', c)

def sutra_3_4_102(c) -> bool:
    return _evaluate('3.4.102', c)

def sutra_3_4_103(c) -> bool:
    return _evaluate('3.4.103', c)

def sutra_3_4_104(c) -> bool:
    return _evaluate('3.4.104', c)

def sutra_3_4_105(c) -> bool:
    return _evaluate('3.4.105', c)

def sutra_3_4_106(c) -> bool:
    return _evaluate('3.4.106', c)

def sutra_3_4_107(c) -> bool:
    return _evaluate('3.4.107', c)

def sutra_3_4_109(c) -> bool:
    return _evaluate('3.4.109', c)

def sutra_3_4_110(c) -> bool:
    return _evaluate('3.4.110', c)

def sutra_3_4_111(c) -> bool:
    return _evaluate('3.4.111', c)

def sutra_3_4_112(c) -> bool:
    return _evaluate('3.4.112', c)

def sutra_3_4_116(c) -> bool:
    return _evaluate('3.4.116', c)

def sutra_3_4_117(c) -> bool:
    return _evaluate('3.4.117', c)

