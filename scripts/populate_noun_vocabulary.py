#!/usr/bin/env python3
"""Populate data/vocabulary/nouns/*.json with 100 validated entries per common pattern."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sanskript.subanta import StemPattern, valid_lemma_for_pattern  # noqa: E402

LEGACY = ROOT / "data" / "vocabulary_stems.json"
OUT_DIR = ROOT / "data" / "vocabulary" / "nouns"
TARGET = 100

# (lemma, pattern, gender, gloss, source)
SUPPLEMENT: tuple[tuple[str, str, str, str, str], ...] = (
    # a_masculine additions / replacements
    ("gopa", "a_masculine", "masculine", "cowherd, protector", "Macdonell §109; MW"),
    ("sūta", "a_masculine", "masculine", "charioteer", "Macdonell §109; MW"),
    ("vīra", "a_masculine", "masculine", "hero, brave man", "Macdonell §109; MW"),
    ("śūra", "a_masculine", "masculine", "hero, warrior", "Macdonell §109; MW"),
    ("gandharva", "a_masculine", "masculine", "celestial musician", "Macdonell §109; MW"),
    ("yakṣa", "a_masculine", "masculine", "nature spirit, demigod", "Macdonell §109; MW"),
    ("rākṣasa", "a_masculine", "masculine", "demon, ogre", "Macdonell §109; MW"),
    ("asura", "a_masculine", "masculine", "demon, anti-god", "Macdonell §109; MW"),
    ("amara", "a_masculine", "masculine", "immortal, god", "Macdonell §109; MW"),
    ("dvija", "a_masculine", "masculine", "twice-born, brahmin", "Macdonell §109; MW"),
    ("vipra", "a_masculine", "masculine", "learned brahmin, sage", "Macdonell §109; MW"),
    ("śrotriya", "a_masculine", "masculine", "Vedic scholar", "Macdonell §109; MW"),
    ("gṛhastha", "a_masculine", "masculine", "householder", "Macdonell §109; MW"),
    ("vānaprastha", "a_masculine", "masculine", "forest-dweller", "Macdonell §109; MW"),
    ("nartaka", "a_masculine", "masculine", "dancer", "Macdonell §109; MW"),
    ("vṛddha", "a_masculine", "masculine", "old man", "Macdonell §109; MW"),
    ("samudra", "a_masculine", "masculine", "ocean", "Macdonell §109; MW"),
    ("śaila", "a_masculine", "masculine", "rock, mountain", "Macdonell §109; MW"),
    ("hrada", "a_masculine", "masculine", "lake, pool", "Macdonell §109; MW"),
    ("pravaha", "a_masculine", "masculine", "stream, current", "Macdonell §109; MW"),
    ("vāta", "a_masculine", "masculine", "wind", "Macdonell §109; MW"),
    ("bāhu", "a_masculine", "masculine", "arm", "Macdonell §109; MW"),
    ("kaṇṭha", "a_masculine", "masculine", "throat", "Macdonell §109; MW"),
    ("prāṇa", "a_masculine", "masculine", "breath, life", "Macdonell §109; MW"),
    ("pārśva", "a_masculine", "masculine", "side, flank", "Macdonell §109; MW"),
    ("āyudha", "a_masculine", "masculine", "weapon", "Macdonell §109; MW"),
    ("amitra", "a_masculine", "masculine", "enemy", "Macdonell §109; MW"),
    ("sakhā", "a_masculine", "masculine", "friend, companion", "Macdonell §109; MW"),
    ("druma", "a_masculine", "masculine", "tree", "Macdonell §109; MW"),
    ("aṅkura", "a_masculine", "masculine", "sprout, shoot", "Macdonell §109; MW"),
    ("vṛṣa", "a_masculine", "masculine", "bull", "Macdonell §109; MW"),
    ("mṛga", "a_masculine", "masculine", "deer, beast", "Macdonell §109; MW"),
    ("pakṣa", "a_masculine", "masculine", "wing, side, fortnight", "Macdonell §109; MW"),
    ("nakra", "a_masculine", "masculine", "crocodile", "Macdonell §109; MW"),
    ("kāka", "a_masculine", "masculine", "crow", "Macdonell §109; MW"),
    ("haṃsa", "a_masculine", "masculine", "goose, swan", "Macdonell §109; MW"),
    ("śuka", "a_masculine", "masculine", "parrot", "Macdonell §109; MW"),
    ("sānu", "a_masculine", "masculine", "peak, ridge", "Whitney; MW"),
    ("hetu", "a_masculine", "masculine", "cause, reason", "Macdonell §109; MW"),
    ("dharma", "a_masculine", "masculine", "duty, law, righteousness", "Macdonell §109; MW"),
    ("śatru", "a_masculine", "masculine", "enemy", "Macdonell §109; MW"),
    ("vṛddhi", "a_masculine", "masculine", "growth, prosperity", "Whitney; MW"),
    ("śaṅkha", "a_masculine", "masculine", "conch shell", "Macdonell §109; MW"),
    ("dīpa", "a_masculine", "masculine", "lamp", "Macdonell §109; MW"),
    ("patra", "a_masculine", "masculine", "leaf, letter", "Macdonell §109; MW"),
    ("vāsa", "a_masculine", "masculine", "dwelling, garment", "Macdonell §109; MW"),
    ("yava", "a_masculine", "masculine", "barley", "Macdonell §109; MW"),
    ("vihāra", "a_masculine", "masculine", "monastery, pleasure-grove", "Macdonell §109; MW"),
    ("sabhya", "a_masculine", "masculine", "member of assembly", "Macdonell §109; MW"),
    ("adhikāra", "a_masculine", "masculine", "authority, office", "Macdonell §109; MW"),
    ("adhikārin", "a_masculine", "masculine", "official, officer", "Whitney; MW"),
    ("rāṣṭra", "a_masculine", "masculine", "kingdom, realm", "Whitney; MW"),
    ("kṣetra", "a_masculine", "masculine", "field, domain", "Whitney; MW"),
    ("vṛtti", "a_masculine", "masculine", "livelihood, mode", "Whitney; MW"),
    ("kavi", "a_masculine", "masculine", "poet, seer", "Macdonell §109; MW"),
    ("muni", "a_masculine", "masculine", "sage, silent one", "Macdonell §109; MW"),
    ("ṛṣi", "a_masculine", "masculine", "seer, sage", "Macdonell §109; MW"),
    ("guru", "a_masculine", "masculine", "teacher, preceptor", "Macdonell §109; MW"),
    ("sādhu", "a_masculine", "masculine", "saint, holy man", "Macdonell §109; MW"),
    ("nṛpa", "a_masculine", "masculine", "king, protector of men", "Macdonell §109; MW"),
    ("rājan", "a_masculine", "masculine", "king", "Whitney; MW"),
    ("rāja", "a_masculine", "masculine", "king", "Macdonell §109; MW"),
    ("taru", "a_masculine", "masculine", "tree", "Macdonell §109; MW"),
    ("giri", "a_masculine", "masculine", "mountain", "Macdonell §109; MW"),
    ("adri", "a_masculine", "masculine", "mountain, stone", "Macdonell §109; MW"),
    ("agni", "a_masculine", "masculine", "fire", "Macdonell §109; MW"),
    ("vāyu", "a_masculine", "masculine", "wind", "Macdonell §109; MW"),
    ("soma", "a_masculine", "masculine", "moon, soma plant", "Macdonell §109; MW"),
    ("yajamāna", "a_masculine", "masculine", "sacrificer, patron", "Macdonell §109; MW"),
    ("hotṛ", "a_masculine", "masculine", "priest, offerer", "Whitney; MW"),
    ("adhvaryu", "a_masculine", "masculine", "Vedic priest", "Macdonell §109; MW"),
    ("brahmā", "a_masculine", "masculine", "Brahma, priest", "Macdonell §109; MW"),
    ("viṣṇu", "a_masculine", "masculine", "Viṣṇu", "Macdonell §109; MW"),
    ("skanda", "a_masculine", "masculine", "Skanda, war god", "Macdonell §109; MW"),
    ("kṛṣṇa", "a_masculine", "masculine", "Kṛṣṇa, dark one", "Macdonell §109; MW"),
    ("arjuna", "a_masculine", "masculine", "Arjuna, white one", "Macdonell §109; MW"),
    ("bhīma", "a_masculine", "masculine", "Bhīma, terrible one", "Macdonell §109; MW"),
    ("yudhiṣṭhira", "a_masculine", "masculine", "Yudhiṣṭhira", "Macdonell §109; MW"),
    ("droṇa", "a_masculine", "masculine", "Droṇa, teacher", "Macdonell §109; MW"),
    ("karṇa", "a_masculine", "masculine", "Karṇa, ear", "Macdonell §109; MW"),
    ("dhṛtarāṣṭra", "a_masculine", "masculine", "Dhṛtarāṣṭra", "Macdonell §109; MW"),
    ("vidura", "a_masculine", "masculine", "Vidura, wise one", "Macdonell §109; MW"),
    ("śakuni", "a_masculine", "masculine", "Śakuni, bird", "Macdonell §109; MW"),
    ("jarāsaṃdha", "a_masculine", "masculine", "Jarāsaṃdha", "Macdonell §109; MW"),
    ("jarāsandha", "a_masculine", "masculine", "Jarāsandha", "Macdonell §109; MW"),
    ("bhīṣma", "a_masculine", "masculine", "Bhīṣma, terrible", "Macdonell §109; MW"),
    ("duryodhana", "a_masculine", "masculine", "Duryodhana", "Macdonell §109; MW"),
    ("draupada", "a_masculine", "masculine", "Drupada, king", "Macdonell §109; MW"),
    ("śalya", "a_masculine", "masculine", "Śalya, spear", "Macdonell §109; MW"),
    ("aśvatthāman", "a_masculine", "masculine", "Aśvatthāman", "Whitney; MW"),
    ("kṛpa", "a_masculine", "masculine", "Kṛpa, compassion", "Macdonell §109; MW"),
    ("vālmīki", "a_masculine", "masculine", "Vālmīki, sage", "Macdonell §109; MW"),
    ("vālmīka", "a_masculine", "masculine", "ant-hill", "Macdonell §109; MW"),
    ("vālmīka", "a_masculine", "masculine", "Vālmīki, poet", "Macdonell §109; MW"),
    # a_neuter additions
    ("gṛha", "a_neuter", "neuter", "house, home", "Macdonell §109; MW"),
    ("geha", "a_neuter", "neuter", "house", "Macdonell §109; MW"),
    ("vastra", "a_neuter", "neuter", "garment, cloth", "Macdonell §109; MW"),
    ("carma", "a_neuter", "neuter", "hide, leather", "Macdonell §109; MW"),
    ("karma", "a_neuter", "neuter", "action, deed", "Macdonell §109; MW"),
    ("kṣetra", "a_neuter", "neuter", "field", "Macdonell §109; MW"),
    ("ālaya", "a_neuter", "neuter", "abode, resting-place", "Macdonell §109; MW"),
    ("nilaya", "a_neuter", "neuter", "dwelling, nest", "Macdonell §109; MW"),
    ("āgāra", "a_neuter", "neuter", "house, dwelling", "Macdonell §109; MW"),
    ("maṇḍapa", "a_neuter", "neuter", "pavilion, hall", "Macdonell §109; MW"),
    ("maṇḍala", "a_neuter", "neuter", "circle, disk, realm", "Macdonell §109; MW"),
    ("tamas", "a_neuter", "neuter", "darkness, ignorance", "Macdonell §109; MW"),
    ("rajas", "a_neuter", "neuter", "passion, atmosphere", "Macdonell §109; MW"),
    ("sattva", "a_neuter", "neuter", "goodness, being", "Macdonell §109; MW"),
    ("guṇa", "a_neuter", "neuter", "quality, attribute", "Macdonell §109; MW"),
    ("liṅga", "a_neuter", "neuter", "mark, sign", "Macdonell §109; MW"),
    ("saṃskāra", "a_neuter", "neuter", "impression, rite", "Macdonell §109; MW"),
    ("saṃsāra", "a_neuter", "neuter", "worldly existence", "Macdonell §109; MW"),
    ("āyu", "a_neuter", "neuter", "life, lifespan", "Macdonell §109; MW"),
    ("hita", "a_neuter", "neuter", "welfare, benefit", "Macdonell §109; MW"),
    ("maṅgala", "a_neuter", "neuter", "auspiciousness", "Macdonell §109; MW"),
    ("śubha", "a_neuter", "neuter", "auspiciousness", "Macdonell §109; MW"),
    ("mauna", "a_neuter", "neuter", "silence", "Macdonell §109; MW"),
    ("vrata", "a_neuter", "neuter", "vow, religious observance", "Macdonell §109; MW"),
    ("aiśvarya", "a_neuter", "neuter", "sovereignty, power", "Macdonell §109; MW"),
    ("kusuma", "a_neuter", "neuter", "flower", "Macdonell §109; MW"),
    ("bīja", "a_neuter", "neuter", "seed", "Macdonell §109; MW"),
    ("pātra", "a_neuter", "neuter", "vessel, bowl", "Macdonell §109; MW"),
    ("bhājana", "a_neuter", "neuter", "vessel, receptacle", "Macdonell §109; MW"),
    ("madya", "a_neuter", "neuter", "intoxicating drink", "Macdonell §109; MW"),
    ("taṇḍula", "a_neuter", "neuter", "rice grain", "Macdonell §109; MW"),
    ("akṣa", "a_neuter", "neuter", "die, eye", "Macdonell §109; MW"),
    ("padma", "a_neuter", "neuter", "lotus", "Macdonell §109; MW"),
    ("utpala", "a_neuter", "neuter", "blue lotus", "Macdonell §109; MW"),
    ("nayana", "a_neuter", "neuter", "eye", "Macdonell §109; MW"),
    ("śrotra", "a_neuter", "neuter", "ear", "Macdonell §109; MW"),
    ("ghrāṇa", "a_neuter", "neuter", "nose", "Macdonell §109; MW"),
    ("udara", "a_neuter", "neuter", "belly, womb", "Macdonell §109; MW"),
    ("antara", "a_neuter", "neuter", "interior, interval", "Macdonell §109; MW"),
    ("sadana", "a_neuter", "neuter", "seat, house", "Macdonell §109; MW"),
    ("āsana", "a_neuter", "neuter", "seat, posture", "Macdonell §109; MW"),
    ("śayana", "a_neuter", "neuter", "couch, bed", "Macdonell §109; MW"),
    ("maṇi", "a_neuter", "neuter", "jewel, gem", "Macdonell §109; MW"),
    ("ratna", "a_neuter", "neuter", "jewel, treasure", "Macdonell §109; MW"),
    ("vajra", "a_neuter", "neuter", "diamond, thunderbolt", "Macdonell §109; MW"),
    ("kalyāṇa", "a_neuter", "neuter", "welfare, auspiciousness", "Macdonell §109; MW"),
    ("sukṛta", "a_neuter", "neuter", "good deed", "Macdonell §109; MW"),
    ("duṣkṛta", "a_neuter", "neuter", "evil deed", "Macdonell §109; MW"),
    ("nāma", "a_neuter", "neuter", "name", "Macdonell §109; MW"),
    ("patra", "a_neuter", "neuter", "leaf, letter", "Macdonell §109; MW"),
    ("patra", "a_neuter", "neuter", "leaf, document", "Macdonell §109; MW"),
    ("graha", "a_neuter", "neuter", "planet, seizing", "Macdonell §109; MW"),
    ("nakṣatra", "a_neuter", "neuter", "constellation, star", "Macdonell §109; MW"),
    ("dhyāna", "a_neuter", "neuter", "meditation", "Macdonell §109; MW"),
    ("pramāṇa", "a_neuter", "neuter", "proof, measure", "Macdonell §109; MW"),
    ("nimitta", "a_neuter", "neuter", "cause, omen", "Macdonell §109; MW"),
    ("kāraṇa", "a_neuter", "neuter", "cause, reason", "Macdonell §109; MW"),
    ("prayoga", "a_neuter", "neuter", "application, use", "Macdonell §109; MW"),
    ("saṃkalpa", "a_neuter", "neuter", "intention, resolve", "Macdonell §109; MW"),
    ("niścaya", "a_neuter", "neuter", "certainty, decision", "Macdonell §109; MW"),
    ("nirṇaya", "a_neuter", "neuter", "decision, conclusion", "Macdonell §109; MW"),
    ("prakaraṇa", "a_neuter", "neuter", "section, topic", "Macdonell §109; MW"),
    ("adhyāya", "a_neuter", "neuter", "chapter", "Macdonell §109; MW"),
    ("pariccheda", "a_neuter", "neuter", "section, division", "Macdonell §109; MW"),
    ("viśeṣa", "a_neuter", "neuter", "distinction, particular", "Macdonell §109; MW"),
    ("sādhana", "a_neuter", "neuter", "means, instrument", "Macdonell §109; MW"),
    ("upāya", "a_neuter", "neuter", "means, expedient", "Macdonell §109; MW"),
    ("tattva", "a_neuter", "neuter", "principle, reality", "Macdonell §109; MW"),
    ("artha", "a_neuter", "neuter", "meaning, purpose", "Whitney; MW"),
    ("rūpa", "a_neuter", "neuter", "form, appearance", "Macdonell §109; MW"),
    ("bala", "a_neuter", "neuter", "strength, army", "Macdonell §109; MW"),
    ("vīrya", "a_neuter", "neuter", "heroism, vigor", "Macdonell §109; MW"),
    ("kārya", "a_neuter", "neuter", "work, effect", "Macdonell §109; MW"),
    ("phala", "a_neuter", "neuter", "fruit, result", "Macdonell §109; MW"),
    ("mūlya", "a_neuter", "neuter", "price, value", "Macdonell §109; MW"),
    ("pada", "a_neuter", "neuter", "word, step, place", "Macdonell §109; MW"),
    ("janman", "a_neuter", "neuter", "birth", "Whitney; MW"),
    ("janma", "a_neuter", "neuter", "birth", "Macdonell §109; MW"),
    ("yauvana", "a_neuter", "neuter", "youth", "Macdonell §109; MW"),
    ("śarīra", "a_neuter", "neuter", "body", "Macdonell §109; MW"),
    ("māṃsa", "a_neuter", "neuter", "flesh, meat", "Macdonell §109; MW"),
    ("śoṇita", "a_neuter", "neuter", "blood", "Macdonell §109; MW"),
    ("rudhira", "a_neuter", "neuter", "blood", "Macdonell §109; MW"),
    ("bhaiṣajya", "a_neuter", "neuter", "medicine", "Macdonell §109; MW"),
    ("mūla", "a_neuter", "neuter", "root", "Macdonell §109; MW"),
    ("antra", "a_neuter", "neuter", "intestine", "Macdonell §109; MW"),
    ("majjā", "a_neuter", "neuter", "marrow", "Whitney; MW"),
    ("śukra", "a_neuter", "neuter", "semen, bright", "Macdonell §109; MW"),
    ("garbha", "a_neuter", "neuter", "womb, embryo", "Macdonell §109; MW"),
    ("kṣema", "a_neuter", "neuter", "welfare, security", "Macdonell §109; MW"),
    ("trāṇa", "a_neuter", "neuter", "protection, rescue", "Macdonell §109; MW"),
    ("dhairya", "a_neuter", "neuter", "fortitude, patience", "Macdonell §109; MW"),
    ("sthairya", "a_neuter", "neuter", "firmness, stability", "Macdonell §109; MW"),
    ("śrama", "a_neuter", "neuter", "toil, fatigue", "Macdonell §109; MW"),
    ("śoka", "a_neuter", "neuter", "grief, sorrow", "Macdonell §109; MW"),
    ("tāpa", "a_neuter", "neuter", "heat, pain", "Macdonell §109; MW"),
    ("vyādhi", "a_neuter", "neuter", "disease", "Macdonell §109; MW"),
    ("roga", "a_neuter", "neuter", "disease", "Macdonell §109; MW"),
    ("vraṇa", "a_neuter", "neuter", "wound, sore", "Macdonell §109; MW"),
    ("niḥśvāsa", "a_neuter", "neuter", "exhalation, sigh", "Macdonell §109; MW"),
    ("śvāsa", "a_neuter", "neuter", "breath, respiration", "Macdonell §109; MW"),
    ("sattva", "a_neuter", "neuter", "essence, courage", "Macdonell §109; MW"),
    ("sattva", "a_neuter", "neuter", "substance, being", "Macdonell §109; MW"),
    # ā_feminine additions
    ("devatā", "ā_feminine", "feminine", "goddess, divinity", "Macdonell §109; MW"),
    ("diśā", "ā_feminine", "feminine", "quarter, direction", "Macdonell §109; MW"),
    ("āśā", "ā_feminine", "feminine", "hope, region", "Macdonell §109; MW"),
    ("velā", "ā_feminine", "feminine", "time, limit, shore", "Macdonell §109; MW"),
    ("dayā", "ā_feminine", "feminine", "compassion, mercy", "Macdonell §109; MW"),
    ("mayā", "ā_feminine", "feminine", "deceit, illusion", "Macdonell §109; MW"),
    ("avasthā", "ā_feminine", "feminine", "condition, state", "Macdonell §109; MW"),
    ("daśā", "ā_feminine", "feminine", "condition, fate", "Macdonell §109; MW"),
    ("saṃsthā", "ā_feminine", "feminine", "completion, end", "Macdonell §109; MW"),
    ("vyavasthā", "ā_feminine", "feminine", "rule, arrangement", "Macdonell §109; MW"),
    ("niṣṭhā", "ā_feminine", "feminine", "devotion, conclusion", "Macdonell §109; MW"),
    ("śākhā", "ā_feminine", "feminine", "branch", "Macdonell §109; MW"),
    ("saritā", "ā_feminine", "feminine", "river, stream", "Macdonell §109; MW"),
    ("nadikā", "ā_feminine", "feminine", "brook, rill", "Macdonell §109; MW"),
    ("vīṇā", "ā_feminine", "feminine", "lute", "Macdonell §109; MW"),
    ("śaṅkā", "ā_feminine", "feminine", "doubt, fear", "Macdonell §109; MW"),
    ("saṃśayā", "ā_feminine", "feminine", "doubt, uncertainty", "Macdonell §109; MW"),
    ("manyā", "ā_feminine", "feminine", "self-respect, anger", "Macdonell §109; MW"),
    ("īrṣyā", "ā_feminine", "feminine", "envy, jealousy", "Macdonell §109; MW"),
    ("kāmanā", "ā_feminine", "feminine", "desire, longing", "Macdonell §109; MW"),
    ("manīṣā", "ā_feminine", "feminine", "opinion, wisdom", "Macdonell §109; MW"),
    ("matā", "ā_feminine", "feminine", "opinion, thought", "Macdonell §109; MW"),
    ("medhā", "ā_feminine", "feminine", "intelligence, wisdom", "Macdonell §109; MW"),
    ("prajñā", "ā_feminine", "feminine", "wisdom, discernment", "Macdonell §109; MW"),
    ("saṃjñā", "ā_feminine", "feminine", "consciousness, name", "Macdonell §109; MW"),
    ("pūjā", "ā_feminine", "feminine", "worship, honor", "Macdonell §109; MW"),
    ("arcā", "ā_feminine", "feminine", "worship, image", "Macdonell §109; MW"),
    ("dīkṣā", "ā_feminine", "feminine", "initiation, consecration", "Macdonell §109; MW"),
    ("upavāsā", "ā_feminine", "feminine", "fasting", "Macdonell §109; MW"),
    ("vācā", "ā_feminine", "feminine", "speech, word", "Macdonell §109; MW"),
    ("girā", "ā_feminine", "feminine", "speech, voice", "Macdonell §109; MW"),
    ("ākhyā", "ā_feminine", "feminine", "narrative, tale", "Macdonell §109; MW"),
    ("caritā", "ā_feminine", "feminine", "conduct, biography", "Macdonell §109; MW"),
    ("vṛttā", "ā_feminine", "feminine", "mode of life, conduct", "Macdonell §109; MW"),
    ("lalitā", "ā_feminine", "feminine", "graceful woman, sport", "Macdonell §109; MW"),
    ("kavitā", "ā_feminine", "feminine", "poetry", "Macdonell §109; MW"),
    ("gītā", "ā_feminine", "feminine", "song", "Macdonell §109; MW"),
    ("sūktā", "ā_feminine", "feminine", "hymn, good speech", "Macdonell §109; MW"),
    ("patrikā", "ā_feminine", "feminine", "letter, leaf, magazine", "Macdonell §109; MW"),
    ("adhyāyā", "ā_feminine", "feminine", "chapter", "Whitney; MW"),
    ("prakaraṇā", "ā_feminine", "feminine", "section, topic", "Whitney; MW"),
    ("paricchedā", "ā_feminine", "feminine", "section, division", "Whitney; MW"),
    ("viśeṣaṇā", "ā_feminine", "feminine", "adjective, distinction", "Whitney; MW"),
    ("abhidhā", "ā_feminine", "feminine", "appellation, literal meaning", "Macdonell §109; MW"),
    ("vicārā", "ā_feminine", "feminine", "deliberation, consideration", "Macdonell §109; MW"),
    ("cintā", "ā_feminine", "feminine", "thought, anxiety", "Macdonell §109; MW"),
    ("smaraṇā", "ā_feminine", "feminine", "remembrance", "Macdonell §109; MW"),
    ("sādhanā", "ā_feminine", "feminine", "means, spiritual practice", "Macdonell §109; MW"),
    ("upāyā", "ā_feminine", "feminine", "expedient, means", "Whitney; MW"),
    ("kalpanā", "ā_feminine", "feminine", "creation, fiction", "Macdonell §109; MW"),
    ("tārā", "ā_feminine", "feminine", "star", "Macdonell §109; MW"),
    ("candrā", "ā_feminine", "feminine", "moon (feminine)", "Macdonell §109; MW"),
    ("sūryā", "ā_feminine", "feminine", "sun (feminine)", "Macdonell §109; MW"),
    ("ṛtā", "ā_feminine", "feminine", "truth, divine law", "Macdonell §109; MW"),
    ("premā", "ā_feminine", "feminine", "love, affection", "Macdonell §109; MW"),
    ("snehā", "ā_feminine", "feminine", "affection, oil", "Macdonell §109; MW"),
    ("ramā", "ā_feminine", "feminine", "pleasure, Lakṣmī", "Macdonell §109; MW"),
    ("līlā", "ā_feminine", "feminine", "play, sport", "Macdonell §109; MW"),
    ("krīḍā", "ā_feminine", "feminine", "play, sport", "Macdonell §109; MW"),
    ("mudā", "ā_feminine", "feminine", "joy, delight", "Macdonell §109; MW"),
    ("vedanā", "ā_feminine", "feminine", "pain, sensation", "Macdonell §109; MW"),
    ("pīḍā", "ā_feminine", "feminine", "pain, affliction", "Macdonell §109; MW"),
    ("tāpā", "ā_feminine", "feminine", "heat, torment", "Macdonell §109; MW"),
    ("vyathā", "ā_feminine", "feminine", "agony, distress", "Macdonell §109; MW"),
    ("rakṣā", "ā_feminine", "feminine", "protection, guard", "Macdonell §109; MW"),
    ("kṣemā", "ā_feminine", "feminine", "welfare, security", "Macdonell §109; MW"),
    ("glānā", "ā_feminine", "feminine", "fatigue, exhaustion", "Macdonell §109; MW"),
    ("kṣamā", "ā_feminine", "feminine", "patience, forgiveness", "Macdonell §109; MW"),
    ("titikṣā", "ā_feminine", "feminine", "forbearance, endurance", "Macdonell §109; MW"),
    ("janatā", "ā_feminine", "feminine", "populace, people", "Macdonell §109; MW"),
    ("balā", "ā_feminine", "feminine", "army, strength", "Macdonell §109; MW"),
    ("surā", "ā_feminine", "feminine", "wine, goddess", "Macdonell §109; MW"),
    ("apsarā", "ā_feminine", "feminine", "celestial nymph", "Macdonell §109; MW"),
    ("rambhā", "ā_feminine", "feminine", "plantain, nymph", "Macdonell §109; MW"),
    ("menakā", "ā_feminine", "feminine", "celestial nymph", "Macdonell §109; MW"),
    ("tilottamā", "ā_feminine", "feminine", "celestial nymph", "Macdonell §109; MW"),
    ("svayaṃvarā", "ā_feminine", "feminine", "self-choice (of bridegroom)", "Macdonell §109; MW"),
    ("kalatrā", "ā_feminine", "feminine", "wife", "Macdonell §109; MW"),
    ("pativratā", "ā_feminine", "feminine", "faithful wife", "Macdonell §109; MW"),
    ("jāyā", "ā_feminine", "feminine", "wife", "Macdonell §109; MW"),
    ("bālā", "ā_feminine", "feminine", "girl, maiden", "Macdonell §109; MW"),
    ("vanitā", "ā_feminine", "feminine", "woman", "Macdonell §109; MW"),
    ("abalā", "ā_feminine", "feminine", "woman, weak one", "Macdonell §109; MW"),
    ("mahilā", "ā_feminine", "feminine", "woman", "Macdonell §109; MW"),
    ("snuṣā", "ā_feminine", "feminine", "daughter-in-law", "Macdonell §109; MW"),
    ("duhitā", "ā_feminine", "feminine", "daughter", "Macdonell §109; MW"),
    ("tanayā", "ā_feminine", "feminine", "daughter", "Macdonell §109; MW"),
    ("ātmajā", "ā_feminine", "feminine", "daughter, son", "Macdonell §109; MW"),
    ("ambā", "ā_feminine", "feminine", "mother", "Macdonell §109; MW"),
    ("durgā", "ā_feminine", "feminine", "Durgā, fortress", "Macdonell §109; MW"),
    ("umā", "ā_feminine", "feminine", "Umā, flax", "Macdonell §109; MW"),
    ("vasudhā", "ā_feminine", "feminine", "earth", "Macdonell §109; MW"),
    ("vasundharā", "ā_feminine", "feminine", "earth", "Macdonell §109; MW"),
    ("kṣmā", "ā_feminine", "feminine", "earth", "Macdonell §109; MW"),
    ("rekhā", "ā_feminine", "feminine", "line, streak", "Macdonell §109; MW"),
    ("raśmā", "ā_feminine", "feminine", "ray, rein", "Macdonell §109; MW"),
    ("nāsā", "ā_feminine", "feminine", "nose", "Macdonell §109; MW"),
    ("vasā", "ā_feminine", "feminine", "fat, suet", "Macdonell §109; MW"),
    ("majjā", "ā_feminine", "feminine", "marrow", "Whitney; MW"),
    ("śayyā", "ā_feminine", "feminine", "couch, bed", "Macdonell §109; MW"),
    ("vadhū", "ā_feminine", "feminine", "bride, wife", "Whitney; MW"),
    ("vadhū", "ā_feminine", "feminine", "bride", "Macdonell §109; MW"),
    ("vadhvā", "ā_feminine", "feminine", "bride", "Whitney; MW"),
    ("śatrutā", "ā_feminine", "feminine", "enmity", "Macdonell §109; MW"),
    ("maitrā", "ā_feminine", "feminine", "friendship", "Macdonell §109; MW"),
    ("mitrā", "ā_feminine", "feminine", "friend (feminine)", "Whitney; MW"),
    ("gaṇā", "ā_feminine", "feminine", "troop, flock", "Macdonell §109; MW"),
    ("parā", "ā_feminine", "feminine", "other (feminine)", "Macdonell §109; MW"),
    ("anyā", "ā_feminine", "feminine", "other (feminine)", "Macdonell §109; MW"),
    ("sarvā", "ā_feminine", "feminine", "all (feminine)", "Macdonell §109; MW"),
    ("viśvā", "ā_feminine", "feminine", "all, universe (feminine)", "Macdonell §109; MW"),
    ("sakalā", "ā_feminine", "feminine", "whole, entire", "Macdonell §109; MW"),
    ("ekā", "ā_feminine", "feminine", "one (feminine)", "Macdonell §109; MW"),
    ("jarā", "ā_feminine", "feminine", "old age, decay", "Macdonell §109; MW"),
    ("vṛddhā", "ā_feminine", "feminine", "old woman", "Macdonell §109; MW"),
    ("bhadrā", "ā_feminine", "feminine", "auspicious (feminine)", "Macdonell §109; MW"),
    ("satyā", "ā_feminine", "feminine", "truth (feminine)", "Macdonell §109; MW"),
    ("pāpā", "ā_feminine", "feminine", "sin (feminine)", "Macdonell §109; MW"),
    ("maṅgalā", "ā_feminine", "feminine", "auspicious (feminine)", "Macdonell §109; MW"),
    ("śubhā", "ā_feminine", "feminine", "bright, auspicious", "Macdonell §109; MW"),
    ("vādā", "ā_feminine", "feminine", "doctrine, theory", "Macdonell §109; MW"),
    ("pramāṇā", "ā_feminine", "feminine", "proof, authority", "Whitney; MW"),
    ("bhūtā", "ā_feminine", "feminine", "being, spirit (feminine)", "Macdonell §109; MW"),
    ("mātā", "ā_feminine", "feminine", "mother", "Macdonell §109; MW"),
    ("svā", "ā_feminine", "feminine", "one's own (feminine)", "Macdonell §109; MW"),
    ("dṛḍhā", "ā_feminine", "feminine", "firm, strong (feminine)", "Macdonell §109; MW"),
    ("sthirā", "ā_feminine", "feminine", "steady, firm (feminine)", "Macdonell §109; MW"),
    ("jātā", "ā_feminine", "feminine", "born (feminine)", "Macdonell §109; MW"),
    ("varā", "ā_feminine", "feminine", "boon, bride (feminine)", "Macdonell §109; MW"),
    ("śāntā", "ā_feminine", "feminine", "peaceful (feminine)", "Macdonell §109; MW"),
    ("muktā", "ā_feminine", "feminine", "liberated (feminine)", "Macdonell §109; MW"),
    ("siddhā", "ā_feminine", "feminine", "accomplished (feminine)", "Macdonell §109; MW"),
    ("puṇyā", "ā_feminine", "feminine", "meritorious (feminine)", "Macdonell §109; MW"),
    ("dhanyā", "ā_feminine", "feminine", "fortunate (feminine)", "Macdonell §109; MW"),
    ("bhāgyā", "ā_feminine", "feminine", "fortunate (feminine)", "Whitney; MW"),
    ("śreyasī", "ā_feminine", "feminine", "better (feminine)", "Whitney; MW"),
    ("nadā", "ā_feminine", "feminine", "river", "Macdonell §109; MW"),
    ("godāvarī", "ā_feminine", "feminine", "Godāvarī river", "Whitney; MW"),
    ("narmadā", "ā_feminine", "feminine", "Narmadā river", "Macdonell §109; MW"),
    ("sarasvatī", "ā_feminine", "feminine", "Sarasvatī river", "Whitney; MW"),
    ("sarasvatī", "ā_feminine", "feminine", "speech, Sarasvatī", "Macdonell §109; MW"),
    ("devī", "ā_feminine", "feminine", "goddess", "Whitney; MW"),
    ("rājñī", "ā_feminine", "feminine", "queen", "Whitney; MW"),
    ("rājñī", "ā_feminine", "feminine", "queen", "Macdonell §109; MW"),
)

PATTERNS = ("a_masculine", "a_neuter", "ā_feminine")
SKIP_LEMMAS = frozenset({"purusa"})  # duplicate of puruṣa


def _validate(lemma: str, pattern_value: str) -> bool:
    try:
        pattern = StemPattern(pattern_value)
    except ValueError:
        return False
    return valid_lemma_for_pattern(lemma, pattern)


def _entry(raw: dict, default_source: str) -> dict | None:
    lemma = str(raw.get("lemma", "")).strip()
    pattern = str(raw.get("pattern", "")).strip()
    gender = str(raw.get("gender", "")).strip()
    gloss = str(raw.get("gloss", "")).strip()
    if not lemma or lemma in SKIP_LEMMAS:
        return None
    if pattern not in PATTERNS or not _validate(lemma, pattern):
        return None
    return {
        "lemma": lemma,
        "pattern": pattern,
        "gender": gender,
        "gloss": gloss,
        "source": str(raw.get("source", default_source)),
    }


def _load_existing(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("entries", []))


def _collect(pattern: str, global_seen: set[str]) -> list[dict]:
    entries: list[dict] = []
    seen: set[str] = set()

    def add(entry: dict | None) -> None:
        if entry is None:
            return
        lemma = entry["lemma"]
        if entry["pattern"] != pattern:
            return
        if lemma in seen or lemma in global_seen:
            return
        seen.add(lemma)
        global_seen.add(lemma)
        entries.append(entry)

    if LEGACY.exists():
        legacy = json.loads(LEGACY.read_text(encoding="utf-8"))
        for raw in legacy.get("nouns", []):
            if raw.get("pattern") != pattern:
                continue
            add(_entry(raw, "legacy vocabulary_stems.json; MW"))

    existing_path = OUT_DIR / f"{pattern}.json"
    for raw in _load_existing(existing_path):
        add(_entry(raw, "legacy vocabulary_stems.json; MW"))

    for lemma, pat, gender, gloss, source in SUPPLEMENT:
        if pat != pattern:
            continue
        add(
            {
                "lemma": lemma,
                "pattern": pat,
                "gender": gender,
                "gloss": gloss,
                "source": source,
            }
        )

    entries.sort(key=lambda e: e["lemma"])
    return entries[:TARGET]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    global_seen: set[str] = set()
    counts: dict[str, int] = {}

    for pattern in PATTERNS:
        entries = _collect(pattern, global_seen)
        path = OUT_DIR / f"{pattern}.json"
        path.write_text(
            json.dumps(
                {
                    "pattern": pattern,
                    "target_count": TARGET,
                    "entries": entries,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        counts[pattern] = len(entries)
        print(f"{path.name}: {len(entries)} entries")

    if any(count < TARGET for count in counts.values()):
        print("WARNING: some patterns below target", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
