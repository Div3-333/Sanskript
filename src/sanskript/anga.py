from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable
from .phonology import (
    best_substitute,
    SOUNDS,
    tokenize_sounds,
    is_vowel,
    is_consonant,
    ArticulationPlace,
    Effort,
    is_ik,
    guna_replacement_for_ik,
    vrddhi_replacement_for_ik,
)


class AngaOperationKind(str, Enum):
    GUNA = "guṇa"
    VRDDHI = "vṛddhi"
    FINAL_LENGTHENING = "final_lengthening"
    AUGMENT = "augment"
    LOPA = "lopa"
    NASALIZATION = "nasalization"
    RETROFLEXION = "retroflexion"


@dataclass(frozen=True)
class AngaOperation:
    name: str
    sutra_range: str
    kind: AngaOperationKind
    source: str
    target: str
    description: str


ANGA_OPERATIONS: tuple[AngaOperation, ...] = (
    AngaOperation("compound-accent-domain", "6.2", AngaOperationKind.AUGMENT, "", "", "records compound-level accent scope"),
    AngaOperation("uttarapada-domain", "6.3", AngaOperationKind.AUGMENT, "", "", "records second-member form scope"),
    AngaOperation("final-a-lengthening", "6.4", AngaOperationKind.FINAL_LENGTHENING, "a", "ā", "lengthens a final stem vowel"),
    AngaOperation("final-lopa", "6.4", AngaOperationKind.LOPA, "a", "", "drops a final stem sound under controlled conditions"),
    AngaOperation("num-augment", "7.1", AngaOperationKind.AUGMENT, "", "n", "adds a controlled nasal augment"),
    AngaOperation("i-guṇa", "7.2", AngaOperationKind.GUNA, "i", "e", "applies guṇa to i/ī"),
    AngaOperation("u-vṛddhi", "7.2", AngaOperationKind.VRDDHI, "u", "au", "applies vṛddhi to u/ū"),
    AngaOperation("ṛ-guṇa", "7.3", AngaOperationKind.GUNA, "ṛ", "ar", "applies guṇa to vocalic ṛ"),
    AngaOperation("n-nasalization", "7.3", AngaOperationKind.NASALIZATION, "n", "ṃ", "records nasalization as an aṅga operation"),
    AngaOperation("ṇati-retroflexion", "7.4", AngaOperationKind.RETROFLEXION, "n", "ṇ", "retroflexes dental n in controlled ṇati domains"),
)


@dataclass(frozen=True)
class Suffix:
    surface: str
    markers: frozenset[str] = field(default_factory=frozenset)
    is_sarvadhatuka: bool = False
    is_ardhadhatuka: bool = False
    is_lit: bool = False
    is_san: bool = False
    is_ktva: bool = False
    is_nistha: bool = False
    is_lin: bool = False
    is_sic: bool = False
    is_atmanepada: bool = False


@dataclass(frozen=True)
class DerivationContext:
    root_lemma: str | None = None
    suffix: Suffix | None = None
    has_dhatu_lopa: bool = False
    is_it_augment: bool = False
    is_bhava_or_adikarma: bool = False

    # Compatibility fields for legacy tests
    is_ardhadhatuka: bool | None = None
    is_kit: bool | None = None
    is_ngit: bool | None = None

    def get_is_kit(self) -> bool:
        """
        Determines if the suffix is treated as 'kit' based on 1.2 rules.
        """
        if self.is_kit is not None:
            return self.is_kit

        if not self.suffix:
            return False

        # Original marker
        if "k" in self.suffix.markers:
            return True

        # 1.2.5: asaṃyogāl-liṭ kit
        if self.suffix.is_lit and "p" not in self.suffix.markers:
            if self.root_lemma:
                sounds = tokenize_sounds(self.root_lemma)
                if len(sounds) >= 2 and not (is_consonant(sounds[-1]) and is_consonant(sounds[-2])):
                    return True
                if len(sounds) == 1:
                    return True

        # 1.2.6: indh-bhavatibhyāṃ ca
        if self.suffix.is_lit and self.root_lemma in {"indh", "bhū"}:
            return True

        # 1.2.7: mṛḍa-mṛda... ktvā
        if self.suffix.is_ktva and self.root_lemma in {"mṛḍ", "mṛd", "gudh", "kuṣ", "kliś", "vad", "vas"}:
            return True

        # 1.2.8: rud-vid... ktvā/san (is kit with iṭ)
        if (self.suffix.is_ktva or self.suffix.is_san) and self.is_it_augment:
            if self.root_lemma in {"rud", "vid", "muṣ", "grah", "svap", "pracch"}:
                return True

        # 1.2.9: iko jhal (san is kit)
        if self.suffix.is_san and self.root_lemma:
            root_sounds = tokenize_sounds(self.root_lemma)
            suffix_sounds = tokenize_sounds(self.suffix.surface)
            if root_sounds and suffix_sounds:
                last_root = root_sounds[-1]
                first_suffix = suffix_sounds[0]
                ik = {"i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ"}
                jhal_blacklist = {"ṅ", "ñ", "ṇ", "n", "m", "y", "r", "l", "v"}
                if last_root in ik and first_suffix not in jhal_blacklist:
                    return True

        # 1.2.11: liṅ-sicāv-ātmanepadeṣu
        if (self.suffix.is_lin or self.suffix.is_sic) and self.suffix.is_atmanepada:
            # 1.2.13: vā gamaḥ
            if self.suffix.is_sic and self.root_lemma == "gam":
                 return True # Simplification: assume 'kit' for now in derivation
            # 1.2.12: uśca (after short ṛ)
            if self.suffix.is_sic and self.root_lemma:
                 root_sounds = tokenize_sounds(self.root_lemma)
                 if root_sounds and root_sounds[-1] == "ṛ":
                     return True
            # 1.2.14: hanah sic
            if self.suffix.is_sic and self.root_lemma == "han":
                return True
            # 1.2.15: yamo gandhane
            if self.suffix.is_sic and self.root_lemma == "yam":
                return True
            # 1.2.17: sthāghvor-icca
            if self.suffix.is_sic and self.root_lemma in {"sthā", "ghu"}:
                return True
            return True

        # 1.2.26: ralo vyupadhād dhalādeḥ saṃśca (optional kit)
        if (self.suffix.is_san or self.suffix.is_ktva) and self.is_it_augment and self.root_lemma:
             sounds = tokenize_sounds(self.root_lemma)
             if len(sounds) >= 3 and is_consonant(sounds[0]):
                  penult = sounds[-2]
                  last = sounds[-1]
                  # ral = all consonants except y, v
                  ral_blacklist = {"y", "v"}
                  # i-u-upadha (i, u, ṛ, ḷ)
                  iu_upadha = {"i", "u", "ṛ", "ḷ"}
                  if penult in iu_upadha and last not in ral_blacklist:
                       return True # optionally kit

        # 1.2.18: na ktvā seṭ (prohibition of kit-tva for ktvā with iṭ)
        if self.suffix.is_ktva and self.is_it_augment:
            return False

        # 1.2.19: niṣṭhā śīṅ-svidi-midi-kṣvidi-dhṛṣaḥ (not kit with iṭ)
        if self.suffix.is_nistha and self.is_it_augment:
             if self.root_lemma in {"śīṅ", "svid", "mid", "kṣvid", "dhṛṣ"}:
                  return False
             # 1.2.20: mṛṣastitikṣāyām
             if self.root_lemma == "mṛṣ":
                  return False

        return False

    def get_is_ngit(self) -> bool:
        """
        Determines if the suffix is treated as 'ṅit' based on 1.2 rules.
        """
        if self.is_ngit is not None:
            return self.is_ngit

        if not self.suffix:
            return False

        # Original marker
        if "ṅ" in self.suffix.markers:
            return True

        # 1.2.1: gāṅ-kuṭādibhyo'ñṇin-ṅit
        if self.root_lemma and (self.root_lemma == "gāṅ" or self.root_lemma.startswith("kuṭ")):
            if "ñ" not in self.suffix.markers and "ṇ" not in self.suffix.markers:
                return True

        # 1.2.2: vije iṭ (iṭ is ṅit)
        if self.root_lemma == "vij" and self.is_it_augment:
             return True

        # 1.2.4: sārvadhātukam-apit
        if self.suffix.is_sarvadhatuka and "p" not in self.suffix.markers:
            return True

        return False


def guna(sound: str, context: DerivationContext | None = None) -> str:
    if context:
        is_ardhadhatuka = context.is_ardhadhatuka if context.is_ardhadhatuka is not None else (context.suffix.is_ardhadhatuka if context.suffix else False)

        # 1.1.4: na dhātulopa ārdhadhātuke
        if context.has_dhatu_lopa and is_ardhadhatuka:
            return sound

        # 1.1.5: kniti ca
        if context.get_is_kit() or context.get_is_ngit():
            return sound

        # 1.1.6: dīdīvevīṭām
        if context.root_lemma in {"dīdī", "vevī"} or (context.is_it_augment and not (context.suffix and context.suffix.is_ktva)):
            return sound

    # 1.1.3: iko guṇavṛddhī restricts this replacement to ik sounds.
    if is_ik(sound):
        return guna_replacement_for_ik(sound)

    # 1.1.2: at eṅ guṇaḥ {a, e, o}
    candidates = ["a", "e", "o"]
    res = best_substitute(sound, candidates)

    # 1.1.51: uraṇ raparaḥ
    if sound in {"ṛ", "ṝ"} and res == "a":
        return "ar"
    if sound == "ḷ" and res == "a":
        return "al"

    return res


def vrddhi(sound: str, context: DerivationContext | None = None) -> str:
    if context:
        is_ardhadhatuka = context.is_ardhadhatuka if context.is_ardhadhatuka is not None else (context.suffix.is_ardhadhatuka if context.suffix else False)

        if context.has_dhatu_lopa and is_ardhadhatuka:
            return sound

        if context.get_is_kit() or context.get_is_ngit():
            return sound

        if context.root_lemma in {"dīdī", "vevī"} or context.is_it_augment:
            return sound

    # 1.1.3: iko guṇavṛddhī restricts this replacement to ik sounds.
    if is_ik(sound):
        return vrddhi_replacement_for_ik(sound)

    # 1.1.1: āt aic vṛddhiḥ {ā, ai, au}
    candidates = ["ā", "ai", "au"]
    res = best_substitute(sound, candidates)

    # 1.1.51: uraṇ raparaḥ
    if sound in {"ṛ", "ṝ"} and res == "ā":
        return "ār"
    if sound == "ḷ" and res == "ā":
        return "āl"

    return res


def operations_for_range(sutra_range: str) -> tuple[AngaOperation, ...]:
    return tuple(operation for operation in ANGA_OPERATIONS if operation.sutra_range == sutra_range)


def operation_named(name: str) -> AngaOperation:
    for operation in ANGA_OPERATIONS:
        if operation.name == name:
            return operation
    raise ValueError(f"Unknown controlled aṅga operation: {name!r}")


def apply_anga_operation(form: str, operation: AngaOperation) -> str:
    if operation.kind == AngaOperationKind.AUGMENT:
        return operation.target + form
    if operation.kind == AngaOperationKind.FINAL_LENGTHENING and form.endswith(operation.source):
        return form[: -len(operation.source)] + operation.target
    if operation.kind == AngaOperationKind.LOPA and form.endswith(operation.source):
        return form[: -len(operation.source)]
    if operation.kind in {AngaOperationKind.GUNA, AngaOperationKind.VRDDHI, AngaOperationKind.NASALIZATION, AngaOperationKind.RETROFLEXION}:
        return form.replace(operation.source, operation.target, 1)
    return form
