from __future__ import annotations


IAST_TO_DEVANAGARI_VOWELS = {
    "a": "अ",
    "ā": "आ",
    "i": "इ",
    "ī": "ई",
    "u": "उ",
    "ū": "ऊ",
    "ṛ": "ऋ",
    "ṝ": "ॠ",
    "ḷ": "ऌ",
    "e": "ए",
    "ai": "ऐ",
    "o": "ओ",
    "au": "औ",
}

IAST_TO_DEVANAGARI_MARKS = {
    "a": "",
    "ā": "ा",
    "i": "ि",
    "ī": "ी",
    "u": "ु",
    "ū": "ू",
    "ṛ": "ृ",
    "ṝ": "ॄ",
    "ḷ": "ॢ",
    "e": "े",
    "ai": "ै",
    "o": "ो",
    "au": "ौ",
}

IAST_TO_DEVANAGARI_CONSONANTS = {
    "kh": "ख",
    "gh": "घ",
    "ch": "छ",
    "jh": "झ",
    "ṭh": "ठ",
    "ḍh": "ढ",
    "th": "थ",
    "dh": "ध",
    "ph": "फ",
    "bh": "भ",
    "k": "क",
    "g": "ग",
    "ṅ": "ङ",
    "c": "च",
    "j": "ज",
    "ñ": "ञ",
    "ṭ": "ट",
    "ḍ": "ड",
    "ṇ": "ण",
    "t": "त",
    "d": "द",
    "n": "न",
    "p": "प",
    "b": "ब",
    "m": "म",
    "y": "य",
    "r": "र",
    "l": "ल",
    "v": "व",
    "ś": "श",
    "ṣ": "ष",
    "s": "स",
    "h": "ह",
}

DEVANAGARI_TO_IAST_VOWELS = {value: key for key, value in IAST_TO_DEVANAGARI_VOWELS.items()}
DEVANAGARI_TO_IAST_MARKS = {value: key for key, value in IAST_TO_DEVANAGARI_MARKS.items() if value}
DEVANAGARI_TO_IAST_CONSONANTS = {value: key for key, value in IAST_TO_DEVANAGARI_CONSONANTS.items()}

DEPENDENT_SIGNS = {
    "ं": "ṃ",
    "ः": "ḥ",
    "ँ": "m̐",
}

IAST_DEPENDENT_SIGNS = {
    "ṃ": "ं",
    "ḥ": "ः",
}

VIRAMA = "्"


def iast_to_devanagari(text: str) -> str:
    tokens = tokenize_iast(text)
    output: list[str] = []
    index = 0

    while index < len(tokens):
        token = tokens[index]
        if token in IAST_TO_DEVANAGARI_CONSONANTS:
            consonant = IAST_TO_DEVANAGARI_CONSONANTS[token]
            next_token = tokens[index + 1] if index + 1 < len(tokens) else None
            if next_token in IAST_TO_DEVANAGARI_MARKS:
                output.append(consonant + IAST_TO_DEVANAGARI_MARKS[next_token])
                index += 2
            else:
                output.append(consonant + VIRAMA)
                index += 1
            continue

        if token in IAST_TO_DEVANAGARI_VOWELS:
            output.append(IAST_TO_DEVANAGARI_VOWELS[token])
        elif token in IAST_DEPENDENT_SIGNS:
            output.append(IAST_DEPENDENT_SIGNS[token])
        else:
            output.append(token)
        index += 1

    return "".join(output)


def devanagari_to_iast(text: str) -> str:
    output: list[str] = []
    index = 0

    while index < len(text):
        char = text[index]
        if char in DEVANAGARI_TO_IAST_CONSONANTS:
            consonant = DEVANAGARI_TO_IAST_CONSONANTS[char]
            next_char = text[index + 1] if index + 1 < len(text) else ""
            if next_char == VIRAMA:
                output.append(consonant)
                index += 2
            elif next_char in DEVANAGARI_TO_IAST_MARKS:
                output.append(consonant + DEVANAGARI_TO_IAST_MARKS[next_char])
                index += 2
            else:
                output.append(consonant + "a")
                index += 1
            continue

        if char in DEVANAGARI_TO_IAST_VOWELS:
            output.append(DEVANAGARI_TO_IAST_VOWELS[char])
        elif char in DEPENDENT_SIGNS:
            output.append(DEPENDENT_SIGNS[char])
        else:
            output.append(char)
        index += 1

    return "".join(output)


def tokenize_iast(text: str) -> list[str]:
    tokens: list[str] = []
    keys = sorted(
        set(IAST_TO_DEVANAGARI_CONSONANTS) | set(IAST_TO_DEVANAGARI_VOWELS) | set(IAST_DEPENDENT_SIGNS),
        key=len,
        reverse=True,
    )
    index = 0
    while index < len(text):
        for key in keys:
            if text.startswith(key, index):
                tokens.append(key)
                index += len(key)
                break
        else:
            tokens.append(text[index])
            index += 1
    return tokens
