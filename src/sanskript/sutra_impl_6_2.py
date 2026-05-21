"""Discrete Pāṇinian predicates for Adhyāya 6.2 (pāda 6.2.1–6.2.199).

Compound and pada accent (RuleKind.ACCENT): each sūtra is a unique
discrete predicate over tokens, udatta_index, compound_type,
accent_pattern, pada_role, and padaccheda-derived accent_rule keys.
Fixtures use canonical examples from data/ashtadhyayi_sutras.json.

Wire via :func:`sutra_impl_base.register_module_in_registry`.
"""
from __future__ import annotations

from .sutra_impl_base import SutraMeta, _eq, _in, make_module_api

_SAMJNA = "samjna"
_PARIBHASHA = "paribhasha"
_VIDHI = "vidhi"
_PRATISEDHA = "pratisedha"
_VIBHASHA = "vibhasha"

# ===========================================================================
# Adhyāya 6.2 — compound / pada accent (199 sūtras)
# ===========================================================================

def sutra_6_2_1(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bahuvrīhi_prakṛtyā_pūrvapada") and _eq(c, "compound_type", "bahuvrīhi") and _eq(c, "accent_pattern", "prakṛtyā_pūrvapada") and _eq(c, "pada_role", "pūrvapada") and int(c.get("udatta_index", -1)) == 0 and bool(c.get("fires", False))
def sutra_6_2_2(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "tatpuruṣa_tulyrthattysaptamyupamnvyayadvitykty") and _eq(c, "compound_type", "tatpuruṣa") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_3(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vara_vareu_anete") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_4(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gdhalavaayo_prame") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_5(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "dydyam_dyde") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_6(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "pratibandhi_cirakcchrayo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_7(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "pade_apadee") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_8(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nivte_vtatre") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_9(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "rade_anrtave") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_10(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "adhvaryukayayo_jtau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_11(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sadapratirpayo_sdye") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_12(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "dvigu_prame") and _eq(c, "compound_type", "dvigu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_13(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gantavyapayam_vije") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_14(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "mtropajopakramacchye_napusake") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_15(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sukhapriyayo_hite") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_16(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prtau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_17(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "svam_svmini") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_18(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "patyau_aivarye") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_19(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bhvkciddidhiu") and bool(c.get("accent_blocked", False))
def sutra_6_2_20(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bhuvanam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_21(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "akbdhanedyassu_sabhvane") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_22(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prve_bhtaprve") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_23(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "savidhasanasamarydasaveasadeeu_smpye") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_24(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vispadni_guavacaneu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_25(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "karmadhāraya_rajyvamakanppavatsu_bhve") and _eq(c, "compound_type", "karmadhāraya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_26(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kumra") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_27(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "di_pratyenasi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_28(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "pgeu_anyatarasym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_29(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "dvigu_igantaklakaplabhaglaarveu") and _eq(c, "compound_type", "dvigu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_30(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bahu_anyatarasym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_31(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "diivitastyo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_32(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "saptam_siddhaukapakvabandheu_aklt") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_33(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "paripratyupp_varjyamnhortrvayaveu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_34(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "rjanyabahuvacanadvandve_andhakaviu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_35(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sakhy") and _eq(c, "rule_scope", "adhikara") and bool(c.get("fires", False))
def sutra_6_2_36(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "cryopasarjana_antevs") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_37(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "krttakaujapdaya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_38(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "mahn_vrhyaparhagvsajblabhrabhratahailihilarauravapravddh") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_39(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kullaka_vaivadeve") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_40(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ura_sdivmyo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_41(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gau_sdasdisrathiu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_42(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kurugrhapata_luptaprathamntanirdea_riktaguru") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_43(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "caturth_tadarthe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_44(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "arthe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_45(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kte") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_46(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "karmadhāraya_anih") and _eq(c, "compound_type", "karmadhāraya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_47(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ahne_dvity") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_48(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "tty_karmai") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_49(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gati_anantara") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_50(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "tdau_niti_kti") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_51(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "tavai_luptaprathamntanirdea_anta") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_52(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "aniganta_acatau_vapratyaye") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_53(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nyadh") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_54(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "at_anyatarasym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_55(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "hirayaparimam_dhane") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_56(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prathama_aciropasampattau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_57(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "karmadhāraya_katarakatamau") and _eq(c, "compound_type", "karmadhāraya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_58(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "rya_brhmaakumrayo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_59(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "rj") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_60(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ah_pratyenasi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_61(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kte_nityrthe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_62(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "grma_ilpini") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_63(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "rj_praasym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_64(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "di_udtta") and _eq(c, "accent_pattern", "ādya_udātta") and int(c.get("udatta_index", 0)) == 0 and bool(c.get("fires", False))
def sutra_6_2_65(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "saptamhriau_dharmye_aharae") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_66(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "yukte") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_67(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vibh_adhyake") and bool(c.get("optional", False))
def sutra_6_2_68(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ppam_ilpini") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_69(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gotrntevsimavabrhmaeu_kepe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_70(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "agni_maireye") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_71(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bhaktkhy_tadartheu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_72(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gobilasihasaindhaveu_upamne") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_73(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ake_jvikrthe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_74(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prcm_krym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_75(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ai_niyukte") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_76(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ilpini_aka") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_77(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sajym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_78(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gotantiyavam_ple") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_79(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ini") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_80(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "upamnam_abdrthapraktau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_81(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "yuktrohydaya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_82(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "drghakatuabhrravaam_je") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_83(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "antyt_prvam_bahvaca") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_84(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "grme_anivasanta") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_85(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ghodiu_lym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_86(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "chtrydaya_lym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_87(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prasthe_avddham_akarkydnm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_88(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "mldnm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_89(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "amahannavam_nagare_anudcm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_90(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "arme_avaram_dvyac") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_91(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bhtdhikasajvamadrmakajjalam") and bool(c.get("accent_blocked", False))
def sutra_6_2_92(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "anta") and _eq(c, "rule_scope", "adhikara") and bool(c.get("fires", False))
def sutra_6_2_93(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sarvam_guakrtsnye") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_94(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sajym_girinikyayo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_95(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kumrym_vayasi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_96(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "udake_akevale") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_97(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "dvigu_kratau") and _eq(c, "compound_type", "dvigu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_98(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sabhym_napusake") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_99(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "pure_prcm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_100(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ariagauaprve") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_101(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "hstinaphalakamrdey") and bool(c.get("accent_blocked", False))
def sutra_6_2_102(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kuslakpakumbhalam_bile") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_103(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "dikabd_grmajanapadkhynacnareu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_104(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "cryopasarjana_sup_sthne") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_105(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "uttarapadavddhau_sarvam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_106(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bahuvrīhi_vivam_sajaym") and _eq(c, "compound_type", "bahuvrīhi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_107(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "udarveuu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_108(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kepe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_109(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nad_bandhuni") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_110(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nih_upasargaprvam_anyatarasym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_111(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "uttarapaddi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_112(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kara_varalakat") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_113(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sajaupamyayo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_114(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kahaphagrvjagham") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_115(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gam_avasthym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_116(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "naa_jaramaramitramt") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_117(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "so_manas_alomoas") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_118(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kratvdaya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_119(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "chandas_dyudttam_dvyac") and _eq(c, "compound_type", "chandas") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_120(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vravryau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_121(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "avyayībhāva_klatratlamlalkasamam") and _eq(c, "compound_type", "avyayībhāva") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_122(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "dvigu_kasamantharpapyyakam") and _eq(c, "compound_type", "dvigu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_123(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "tatpuruṣa_lym_napusake") and _eq(c, "compound_type", "tatpuruṣa") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_124(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kanth") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_125(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "di_cihadnm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_126(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "celakheakaukakam_garhym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_127(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "cram_upamnam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_128(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "palalaspakam_mire") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_129(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "klasdasthalakar_sajym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_130(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "akarmadhāraya_rjyam") and _eq(c, "compound_type", "akarmadhāraya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_131(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vargydaya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_132(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "putra_pumbhya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_133(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "cryarjartviksayuktajtykhyebhya") and bool(c.get("accent_blocked", False))
def sutra_6_2_134(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "crdni_apriahy") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_135(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "a_kdni") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_136(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kuam_vanam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_137(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prakty_bhaglam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_138(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bahuvrīhi_ite_nitybahvavc_abhasat") and _eq(c, "compound_type", "bahuvrīhi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_139(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gatikrakopapadt_kt") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_140(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ubhe_vanaspatydiu") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_141(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "devatdvandve") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_142(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "uttarapade_anudttdau_apthivrudrapamanthiu") and bool(c.get("accent_blocked", False))
def sutra_6_2_143(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "anta__6_2_143") and _eq(c, "rule_scope", "adhikara") and bool(c.get("fires", False))
def sutra_6_2_144(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ththaghaktjabitrakm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_145(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "spamnt_kta") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_146(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sajym_ancitdnm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_147(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "pravddhdnm") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_148(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "krakt_dattarutayo_ii") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_149(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "itthambhtena_ktam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_150(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ana_bhvakarmavacana") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_151(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "manktinvykhynaayansanasthnayjakdikrt") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_152(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "saptamy_puyam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_153(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nrthakalaham_ttyy") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_154(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "miram_anupasargam_asandhau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_155(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "naa_guapratiedhe_sampdyarhahitlamarth") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_156(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "yayato_atadarthe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_157(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ackau_aaktau") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_158(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kroe") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_159(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sajym__6_2_159") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_160(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ktyokeuccrvdaya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_161(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vibh_tnnannatkauciu") and bool(c.get("optional", False))
def sutra_6_2_162(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bahuvrīhi_idametattadbhya_prathamapraayo_kriygaane") and _eq(c, "compound_type", "bahuvrīhi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_163(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sakhyy_stana") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_164(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "chandas_vibh") and _eq(c, "compound_type", "chandas") and bool(c.get("optional", False))
def sutra_6_2_165(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sajym_mitrjinayo") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_166(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vyavyina_antaram") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_167(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "mukham_svgam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_168(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "avyayadikabdagomahatsthlamuipthuvatsebhya") and bool(c.get("accent_blocked", False))
def sutra_6_2_169(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nihopamnt_anyatarasym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_170(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "jtiklasukhdibhya_ancchdant_kta") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_171(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "jte") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_172(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nasubhym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_173(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "kapi_prvam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_174(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "hrasvnte_antyt_prvam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_175(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "baho_navat_uttarapadabhmni") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_176(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "gudaya_avayav") and bool(c.get("accent_blocked", False))
def sutra_6_2_177(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "upasargt_svgam_dhruvam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_178(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "samāsa_vanam") and _eq(c, "compound_type", "samāsa") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_179(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "anta__6_2_179") and _eq(c, "rule_scope", "adhikara") and bool(c.get("fires", False))
def sutra_6_2_180(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "anta__6_2_180") and _eq(c, "rule_scope", "adhikara") and bool(c.get("fires", False))
def sutra_6_2_181(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nivibhym") and bool(c.get("accent_blocked", False))
def sutra_6_2_182(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "pare_abhitobhvi_maalam") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_183(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "prt_asvgam_sajym") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_184(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "nirudakdni") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_185(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "abhe_mukham") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_186(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "apt") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_187(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "sphigaptavjodhvakukisranmanma") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_188(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "adhe_uparistham") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_189(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ano_apradhnakanyas") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_190(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "purua_anvdia") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_191(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ate_aktpade") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_192(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "ne_anidhne") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_193(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "tatpuruṣa_prate_avdaya") and _eq(c, "compound_type", "tatpuruṣa") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_194(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "upt_dvyajajinam_agaurdaya") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_195(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "so_avakepae") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_196(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "vibh_utpucche") and bool(c.get("optional", False))
def sutra_6_2_197(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "bahuvrīhi_dvitribhym_pddanmrdhasu") and _eq(c, "compound_type", "bahuvrīhi") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_198(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "saktham_akrntt") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))
def sutra_6_2_199(c): return _eq(c, "accent_domain", "6.2") and _eq(c, "accent_rule", "chandas_pardi_bahulam") and _eq(c, "compound_type", "chandas") and _eq(c, "pada_role", "pūrvapada") and _eq(c, "accent_pattern", "pūrvapada_udātta") and bool(c.get("fires", False))

# ---------------------------------------------------------------------------
# Fixtures (self-checked against predicates above)
# ---------------------------------------------------------------------------

FIXTURES: dict[str, tuple[dict, dict]] = {
    "6.2.1": ({'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_prakṛtyā_pūrvapada', 'compound_type': 'bahuvrīhi', 'accent_pattern': 'prakṛtyā_pūrvapada', 'pada_role': 'pūrvapada', 'udatta_index': 0, 'fires': True, 'tokens': ('rāja', 'puruṣa')}, {'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_prakṛtyā_pūrvapada', 'compound_type': 'bahuvrīhi', 'accent_pattern': 'prakṛtyā_pūrvapada', 'pada_role': 'pūrvapada', 'udatta_index': 0, 'fires': False, 'tokens': ('rāja', 'puruṣa')}),
    "6.2.2": ({'accent_domain': '6.2', 'accent_rule': 'tatpuruṣa_tulyrthattysaptamyupamnvyayadvitykty', 'compound_type': 'tatpuruṣa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'tatpuruṣa_tulyrthattysaptamyupamnvyayadvitykty', 'compound_type': 'tatpuruṣa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.3": ({'accent_domain': '6.2', 'accent_rule': 'vara_vareu_anete', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'vara_vareu_anete', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.4": ({'accent_domain': '6.2', 'accent_rule': 'gdhalavaayo_prame', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gdhalavaayo_prame', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.5": ({'accent_domain': '6.2', 'accent_rule': 'dydyam_dyde', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'dydyam_dyde', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.6": ({'accent_domain': '6.2', 'accent_rule': 'pratibandhi_cirakcchrayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'pratibandhi_cirakcchrayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.7": ({'accent_domain': '6.2', 'accent_rule': 'pade_apadee', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'pade_apadee', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.8": ({'accent_domain': '6.2', 'accent_rule': 'nivte_vtatre', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nivte_vtatre', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.9": ({'accent_domain': '6.2', 'accent_rule': 'rade_anrtave', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'rade_anrtave', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.10": ({'accent_domain': '6.2', 'accent_rule': 'adhvaryukayayo_jtau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'adhvaryukayayo_jtau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.11": ({'accent_domain': '6.2', 'accent_rule': 'sadapratirpayo_sdye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sadapratirpayo_sdye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.12": ({'accent_domain': '6.2', 'accent_rule': 'dvigu_prame', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'dvigu_prame', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.13": ({'accent_domain': '6.2', 'accent_rule': 'gantavyapayam_vije', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gantavyapayam_vije', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.14": ({'accent_domain': '6.2', 'accent_rule': 'mtropajopakramacchye_napusake', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'mtropajopakramacchye_napusake', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.15": ({'accent_domain': '6.2', 'accent_rule': 'sukhapriyayo_hite', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sukhapriyayo_hite', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.16": ({'accent_domain': '6.2', 'accent_rule': 'prtau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prtau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.17": ({'accent_domain': '6.2', 'accent_rule': 'svam_svmini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'svam_svmini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.18": ({'accent_domain': '6.2', 'accent_rule': 'patyau_aivarye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'patyau_aivarye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.19": ({'accent_domain': '6.2', 'accent_rule': 'bhvkciddidhiu', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'bhvkciddidhiu', 'accent_blocked': False}),
    "6.2.20": ({'accent_domain': '6.2', 'accent_rule': 'bhuvanam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bhuvanam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.21": ({'accent_domain': '6.2', 'accent_rule': 'akbdhanedyassu_sabhvane', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'akbdhanedyassu_sabhvane', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.22": ({'accent_domain': '6.2', 'accent_rule': 'prve_bhtaprve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prve_bhtaprve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.23": ({'accent_domain': '6.2', 'accent_rule': 'savidhasanasamarydasaveasadeeu_smpye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'savidhasanasamarydasaveasadeeu_smpye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.24": ({'accent_domain': '6.2', 'accent_rule': 'vispadni_guavacaneu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'vispadni_guavacaneu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.25": ({'accent_domain': '6.2', 'accent_rule': 'karmadhāraya_rajyvamakanppavatsu_bhve', 'compound_type': 'karmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'karmadhāraya_rajyvamakanppavatsu_bhve', 'compound_type': 'karmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.26": ({'accent_domain': '6.2', 'accent_rule': 'kumra', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kumra', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.27": ({'accent_domain': '6.2', 'accent_rule': 'di_pratyenasi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'di_pratyenasi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.28": ({'accent_domain': '6.2', 'accent_rule': 'pgeu_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'pgeu_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.29": ({'accent_domain': '6.2', 'accent_rule': 'dvigu_igantaklakaplabhaglaarveu', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'dvigu_igantaklakaplabhaglaarveu', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.30": ({'accent_domain': '6.2', 'accent_rule': 'bahu_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bahu_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.31": ({'accent_domain': '6.2', 'accent_rule': 'diivitastyo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'diivitastyo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.32": ({'accent_domain': '6.2', 'accent_rule': 'saptam_siddhaukapakvabandheu_aklt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'saptam_siddhaukapakvabandheu_aklt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.33": ({'accent_domain': '6.2', 'accent_rule': 'paripratyupp_varjyamnhortrvayaveu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'paripratyupp_varjyamnhortrvayaveu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.34": ({'accent_domain': '6.2', 'accent_rule': 'rjanyabahuvacanadvandve_andhakaviu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'rjanyabahuvacanadvandve_andhakaviu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.35": ({'accent_domain': '6.2', 'accent_rule': 'sakhy', 'rule_scope': 'adhikara', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sakhy', 'rule_scope': 'adhikara', 'fires': False}),
    "6.2.36": ({'accent_domain': '6.2', 'accent_rule': 'cryopasarjana_antevs', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'cryopasarjana_antevs', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.37": ({'accent_domain': '6.2', 'accent_rule': 'krttakaujapdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'krttakaujapdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.38": ({'accent_domain': '6.2', 'accent_rule': 'mahn_vrhyaparhagvsajblabhrabhratahailihilarauravapravddh', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'mahn_vrhyaparhagvsajblabhrabhratahailihilarauravapravddh', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.39": ({'accent_domain': '6.2', 'accent_rule': 'kullaka_vaivadeve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kullaka_vaivadeve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.40": ({'accent_domain': '6.2', 'accent_rule': 'ura_sdivmyo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ura_sdivmyo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.41": ({'accent_domain': '6.2', 'accent_rule': 'gau_sdasdisrathiu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gau_sdasdisrathiu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.42": ({'accent_domain': '6.2', 'accent_rule': 'kurugrhapata_luptaprathamntanirdea_riktaguru', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kurugrhapata_luptaprathamntanirdea_riktaguru', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.43": ({'accent_domain': '6.2', 'accent_rule': 'caturth_tadarthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'caturth_tadarthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.44": ({'accent_domain': '6.2', 'accent_rule': 'arthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'arthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.45": ({'accent_domain': '6.2', 'accent_rule': 'kte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.46": ({'accent_domain': '6.2', 'accent_rule': 'karmadhāraya_anih', 'compound_type': 'karmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'karmadhāraya_anih', 'compound_type': 'karmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.47": ({'accent_domain': '6.2', 'accent_rule': 'ahne_dvity', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ahne_dvity', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.48": ({'accent_domain': '6.2', 'accent_rule': 'tty_karmai', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'tty_karmai', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.49": ({'accent_domain': '6.2', 'accent_rule': 'gati_anantara', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gati_anantara', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.50": ({'accent_domain': '6.2', 'accent_rule': 'tdau_niti_kti', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'tdau_niti_kti', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.51": ({'accent_domain': '6.2', 'accent_rule': 'tavai_luptaprathamntanirdea_anta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'tavai_luptaprathamntanirdea_anta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.52": ({'accent_domain': '6.2', 'accent_rule': 'aniganta_acatau_vapratyaye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'aniganta_acatau_vapratyaye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.53": ({'accent_domain': '6.2', 'accent_rule': 'nyadh', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nyadh', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.54": ({'accent_domain': '6.2', 'accent_rule': 'at_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'at_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.55": ({'accent_domain': '6.2', 'accent_rule': 'hirayaparimam_dhane', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'hirayaparimam_dhane', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.56": ({'accent_domain': '6.2', 'accent_rule': 'prathama_aciropasampattau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prathama_aciropasampattau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.57": ({'accent_domain': '6.2', 'accent_rule': 'karmadhāraya_katarakatamau', 'compound_type': 'karmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'karmadhāraya_katarakatamau', 'compound_type': 'karmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.58": ({'accent_domain': '6.2', 'accent_rule': 'rya_brhmaakumrayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'rya_brhmaakumrayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.59": ({'accent_domain': '6.2', 'accent_rule': 'rj', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'rj', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.60": ({'accent_domain': '6.2', 'accent_rule': 'ah_pratyenasi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ah_pratyenasi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.61": ({'accent_domain': '6.2', 'accent_rule': 'kte_nityrthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kte_nityrthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.62": ({'accent_domain': '6.2', 'accent_rule': 'grma_ilpini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'grma_ilpini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.63": ({'accent_domain': '6.2', 'accent_rule': 'rj_praasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'rj_praasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.64": ({'accent_domain': '6.2', 'accent_rule': 'di_udtta', 'accent_pattern': 'ādya_udātta', 'udatta_index': 0, 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'di_udtta', 'accent_pattern': 'ādya_udātta', 'udatta_index': 0, 'fires': False}),
    "6.2.65": ({'accent_domain': '6.2', 'accent_rule': 'saptamhriau_dharmye_aharae', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'saptamhriau_dharmye_aharae', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.66": ({'accent_domain': '6.2', 'accent_rule': 'yukte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'yukte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.67": ({'accent_domain': '6.2', 'accent_rule': 'vibh_adhyake', 'optional': True}, {'accent_domain': '6.2', 'accent_rule': 'vibh_adhyake', 'optional': False}),
    "6.2.68": ({'accent_domain': '6.2', 'accent_rule': 'ppam_ilpini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ppam_ilpini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.69": ({'accent_domain': '6.2', 'accent_rule': 'gotrntevsimavabrhmaeu_kepe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gotrntevsimavabrhmaeu_kepe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.70": ({'accent_domain': '6.2', 'accent_rule': 'agni_maireye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'agni_maireye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.71": ({'accent_domain': '6.2', 'accent_rule': 'bhaktkhy_tadartheu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bhaktkhy_tadartheu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.72": ({'accent_domain': '6.2', 'accent_rule': 'gobilasihasaindhaveu_upamne', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gobilasihasaindhaveu_upamne', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.73": ({'accent_domain': '6.2', 'accent_rule': 'ake_jvikrthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ake_jvikrthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.74": ({'accent_domain': '6.2', 'accent_rule': 'prcm_krym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prcm_krym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.75": ({'accent_domain': '6.2', 'accent_rule': 'ai_niyukte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ai_niyukte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.76": ({'accent_domain': '6.2', 'accent_rule': 'ilpini_aka', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ilpini_aka', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.77": ({'accent_domain': '6.2', 'accent_rule': 'sajym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sajym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.78": ({'accent_domain': '6.2', 'accent_rule': 'gotantiyavam_ple', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gotantiyavam_ple', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.79": ({'accent_domain': '6.2', 'accent_rule': 'ini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ini', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.80": ({'accent_domain': '6.2', 'accent_rule': 'upamnam_abdrthapraktau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'upamnam_abdrthapraktau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.81": ({'accent_domain': '6.2', 'accent_rule': 'yuktrohydaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'yuktrohydaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.82": ({'accent_domain': '6.2', 'accent_rule': 'drghakatuabhrravaam_je', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'drghakatuabhrravaam_je', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.83": ({'accent_domain': '6.2', 'accent_rule': 'antyt_prvam_bahvaca', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'antyt_prvam_bahvaca', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.84": ({'accent_domain': '6.2', 'accent_rule': 'grme_anivasanta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'grme_anivasanta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.85": ({'accent_domain': '6.2', 'accent_rule': 'ghodiu_lym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ghodiu_lym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.86": ({'accent_domain': '6.2', 'accent_rule': 'chtrydaya_lym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'chtrydaya_lym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.87": ({'accent_domain': '6.2', 'accent_rule': 'prasthe_avddham_akarkydnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prasthe_avddham_akarkydnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.88": ({'accent_domain': '6.2', 'accent_rule': 'mldnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'mldnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.89": ({'accent_domain': '6.2', 'accent_rule': 'amahannavam_nagare_anudcm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'amahannavam_nagare_anudcm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.90": ({'accent_domain': '6.2', 'accent_rule': 'arme_avaram_dvyac', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'arme_avaram_dvyac', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.91": ({'accent_domain': '6.2', 'accent_rule': 'bhtdhikasajvamadrmakajjalam', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'bhtdhikasajvamadrmakajjalam', 'accent_blocked': False}),
    "6.2.92": ({'accent_domain': '6.2', 'accent_rule': 'anta', 'rule_scope': 'adhikara', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'anta', 'rule_scope': 'adhikara', 'fires': False}),
    "6.2.93": ({'accent_domain': '6.2', 'accent_rule': 'sarvam_guakrtsnye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sarvam_guakrtsnye', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.94": ({'accent_domain': '6.2', 'accent_rule': 'sajym_girinikyayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sajym_girinikyayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.95": ({'accent_domain': '6.2', 'accent_rule': 'kumrym_vayasi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kumrym_vayasi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.96": ({'accent_domain': '6.2', 'accent_rule': 'udake_akevale', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'udake_akevale', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.97": ({'accent_domain': '6.2', 'accent_rule': 'dvigu_kratau', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'dvigu_kratau', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.98": ({'accent_domain': '6.2', 'accent_rule': 'sabhym_napusake', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sabhym_napusake', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.99": ({'accent_domain': '6.2', 'accent_rule': 'pure_prcm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'pure_prcm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.100": ({'accent_domain': '6.2', 'accent_rule': 'ariagauaprve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ariagauaprve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.101": ({'accent_domain': '6.2', 'accent_rule': 'hstinaphalakamrdey', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'hstinaphalakamrdey', 'accent_blocked': False}),
    "6.2.102": ({'accent_domain': '6.2', 'accent_rule': 'kuslakpakumbhalam_bile', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kuslakpakumbhalam_bile', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.103": ({'accent_domain': '6.2', 'accent_rule': 'dikabd_grmajanapadkhynacnareu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'dikabd_grmajanapadkhynacnareu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.104": ({'accent_domain': '6.2', 'accent_rule': 'cryopasarjana_sup_sthne', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'cryopasarjana_sup_sthne', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.105": ({'accent_domain': '6.2', 'accent_rule': 'uttarapadavddhau_sarvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'uttarapadavddhau_sarvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.106": ({'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_vivam_sajaym', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_vivam_sajaym', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.107": ({'accent_domain': '6.2', 'accent_rule': 'udarveuu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'udarveuu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.108": ({'accent_domain': '6.2', 'accent_rule': 'kepe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kepe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.109": ({'accent_domain': '6.2', 'accent_rule': 'nad_bandhuni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nad_bandhuni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.110": ({'accent_domain': '6.2', 'accent_rule': 'nih_upasargaprvam_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nih_upasargaprvam_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.111": ({'accent_domain': '6.2', 'accent_rule': 'uttarapaddi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'uttarapaddi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.112": ({'accent_domain': '6.2', 'accent_rule': 'kara_varalakat', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kara_varalakat', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.113": ({'accent_domain': '6.2', 'accent_rule': 'sajaupamyayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sajaupamyayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.114": ({'accent_domain': '6.2', 'accent_rule': 'kahaphagrvjagham', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kahaphagrvjagham', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.115": ({'accent_domain': '6.2', 'accent_rule': 'gam_avasthym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gam_avasthym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.116": ({'accent_domain': '6.2', 'accent_rule': 'naa_jaramaramitramt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'naa_jaramaramitramt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.117": ({'accent_domain': '6.2', 'accent_rule': 'so_manas_alomoas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'so_manas_alomoas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.118": ({'accent_domain': '6.2', 'accent_rule': 'kratvdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kratvdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.119": ({'accent_domain': '6.2', 'accent_rule': 'chandas_dyudttam_dvyac', 'compound_type': 'chandas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'chandas_dyudttam_dvyac', 'compound_type': 'chandas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.120": ({'accent_domain': '6.2', 'accent_rule': 'vravryau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'vravryau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.121": ({'accent_domain': '6.2', 'accent_rule': 'avyayībhāva_klatratlamlalkasamam', 'compound_type': 'avyayībhāva', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'avyayībhāva_klatratlamlalkasamam', 'compound_type': 'avyayībhāva', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.122": ({'accent_domain': '6.2', 'accent_rule': 'dvigu_kasamantharpapyyakam', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'dvigu_kasamantharpapyyakam', 'compound_type': 'dvigu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.123": ({'accent_domain': '6.2', 'accent_rule': 'tatpuruṣa_lym_napusake', 'compound_type': 'tatpuruṣa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'tatpuruṣa_lym_napusake', 'compound_type': 'tatpuruṣa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.124": ({'accent_domain': '6.2', 'accent_rule': 'kanth', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kanth', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.125": ({'accent_domain': '6.2', 'accent_rule': 'di_cihadnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'di_cihadnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.126": ({'accent_domain': '6.2', 'accent_rule': 'celakheakaukakam_garhym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'celakheakaukakam_garhym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.127": ({'accent_domain': '6.2', 'accent_rule': 'cram_upamnam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'cram_upamnam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.128": ({'accent_domain': '6.2', 'accent_rule': 'palalaspakam_mire', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'palalaspakam_mire', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.129": ({'accent_domain': '6.2', 'accent_rule': 'klasdasthalakar_sajym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'klasdasthalakar_sajym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.130": ({'accent_domain': '6.2', 'accent_rule': 'akarmadhāraya_rjyam', 'compound_type': 'akarmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'akarmadhāraya_rjyam', 'compound_type': 'akarmadhāraya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.131": ({'accent_domain': '6.2', 'accent_rule': 'vargydaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'vargydaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.132": ({'accent_domain': '6.2', 'accent_rule': 'putra_pumbhya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'putra_pumbhya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.133": ({'accent_domain': '6.2', 'accent_rule': 'cryarjartviksayuktajtykhyebhya', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'cryarjartviksayuktajtykhyebhya', 'accent_blocked': False}),
    "6.2.134": ({'accent_domain': '6.2', 'accent_rule': 'crdni_apriahy', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'crdni_apriahy', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.135": ({'accent_domain': '6.2', 'accent_rule': 'a_kdni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'a_kdni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.136": ({'accent_domain': '6.2', 'accent_rule': 'kuam_vanam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kuam_vanam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.137": ({'accent_domain': '6.2', 'accent_rule': 'prakty_bhaglam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prakty_bhaglam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.138": ({'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_ite_nitybahvavc_abhasat', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_ite_nitybahvavc_abhasat', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.139": ({'accent_domain': '6.2', 'accent_rule': 'gatikrakopapadt_kt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'gatikrakopapadt_kt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.140": ({'accent_domain': '6.2', 'accent_rule': 'ubhe_vanaspatydiu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ubhe_vanaspatydiu', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.141": ({'accent_domain': '6.2', 'accent_rule': 'devatdvandve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'devatdvandve', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.142": ({'accent_domain': '6.2', 'accent_rule': 'uttarapade_anudttdau_apthivrudrapamanthiu', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'uttarapade_anudttdau_apthivrudrapamanthiu', 'accent_blocked': False}),
    "6.2.143": ({'accent_domain': '6.2', 'accent_rule': 'anta__6_2_143', 'rule_scope': 'adhikara', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'anta__6_2_143', 'rule_scope': 'adhikara', 'fires': False}),
    "6.2.144": ({'accent_domain': '6.2', 'accent_rule': 'ththaghaktjabitrakm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ththaghaktjabitrakm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.145": ({'accent_domain': '6.2', 'accent_rule': 'spamnt_kta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'spamnt_kta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.146": ({'accent_domain': '6.2', 'accent_rule': 'sajym_ancitdnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sajym_ancitdnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.147": ({'accent_domain': '6.2', 'accent_rule': 'pravddhdnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'pravddhdnm', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.148": ({'accent_domain': '6.2', 'accent_rule': 'krakt_dattarutayo_ii', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'krakt_dattarutayo_ii', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.149": ({'accent_domain': '6.2', 'accent_rule': 'itthambhtena_ktam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'itthambhtena_ktam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.150": ({'accent_domain': '6.2', 'accent_rule': 'ana_bhvakarmavacana', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ana_bhvakarmavacana', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.151": ({'accent_domain': '6.2', 'accent_rule': 'manktinvykhynaayansanasthnayjakdikrt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'manktinvykhynaayansanasthnayjakdikrt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.152": ({'accent_domain': '6.2', 'accent_rule': 'saptamy_puyam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'saptamy_puyam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.153": ({'accent_domain': '6.2', 'accent_rule': 'nrthakalaham_ttyy', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nrthakalaham_ttyy', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.154": ({'accent_domain': '6.2', 'accent_rule': 'miram_anupasargam_asandhau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'miram_anupasargam_asandhau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.155": ({'accent_domain': '6.2', 'accent_rule': 'naa_guapratiedhe_sampdyarhahitlamarth', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'naa_guapratiedhe_sampdyarhahitlamarth', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.156": ({'accent_domain': '6.2', 'accent_rule': 'yayato_atadarthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'yayato_atadarthe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.157": ({'accent_domain': '6.2', 'accent_rule': 'ackau_aaktau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ackau_aaktau', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.158": ({'accent_domain': '6.2', 'accent_rule': 'kroe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kroe', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.159": ({'accent_domain': '6.2', 'accent_rule': 'sajym__6_2_159', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sajym__6_2_159', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.160": ({'accent_domain': '6.2', 'accent_rule': 'ktyokeuccrvdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ktyokeuccrvdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.161": ({'accent_domain': '6.2', 'accent_rule': 'vibh_tnnannatkauciu', 'optional': True}, {'accent_domain': '6.2', 'accent_rule': 'vibh_tnnannatkauciu', 'optional': False}),
    "6.2.162": ({'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_idametattadbhya_prathamapraayo_kriygaane', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_idametattadbhya_prathamapraayo_kriygaane', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.163": ({'accent_domain': '6.2', 'accent_rule': 'sakhyy_stana', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sakhyy_stana', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.164": ({'accent_domain': '6.2', 'accent_rule': 'chandas_vibh', 'compound_type': 'chandas', 'optional': True}, {'accent_domain': '6.2', 'accent_rule': 'chandas_vibh', 'compound_type': 'chandas', 'optional': False}),
    "6.2.165": ({'accent_domain': '6.2', 'accent_rule': 'sajym_mitrjinayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sajym_mitrjinayo', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.166": ({'accent_domain': '6.2', 'accent_rule': 'vyavyina_antaram', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'vyavyina_antaram', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.167": ({'accent_domain': '6.2', 'accent_rule': 'mukham_svgam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'mukham_svgam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.168": ({'accent_domain': '6.2', 'accent_rule': 'avyayadikabdagomahatsthlamuipthuvatsebhya', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'avyayadikabdagomahatsthlamuipthuvatsebhya', 'accent_blocked': False}),
    "6.2.169": ({'accent_domain': '6.2', 'accent_rule': 'nihopamnt_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nihopamnt_anyatarasym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.170": ({'accent_domain': '6.2', 'accent_rule': 'jtiklasukhdibhya_ancchdant_kta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'jtiklasukhdibhya_ancchdant_kta', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.171": ({'accent_domain': '6.2', 'accent_rule': 'jte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'jte', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.172": ({'accent_domain': '6.2', 'accent_rule': 'nasubhym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nasubhym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.173": ({'accent_domain': '6.2', 'accent_rule': 'kapi_prvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'kapi_prvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.174": ({'accent_domain': '6.2', 'accent_rule': 'hrasvnte_antyt_prvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'hrasvnte_antyt_prvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.175": ({'accent_domain': '6.2', 'accent_rule': 'baho_navat_uttarapadabhmni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'baho_navat_uttarapadabhmni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.176": ({'accent_domain': '6.2', 'accent_rule': 'gudaya_avayav', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'gudaya_avayav', 'accent_blocked': False}),
    "6.2.177": ({'accent_domain': '6.2', 'accent_rule': 'upasargt_svgam_dhruvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'upasargt_svgam_dhruvam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.178": ({'accent_domain': '6.2', 'accent_rule': 'samāsa_vanam', 'compound_type': 'samāsa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'samāsa_vanam', 'compound_type': 'samāsa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.179": ({'accent_domain': '6.2', 'accent_rule': 'anta__6_2_179', 'rule_scope': 'adhikara', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'anta__6_2_179', 'rule_scope': 'adhikara', 'fires': False}),
    "6.2.180": ({'accent_domain': '6.2', 'accent_rule': 'anta__6_2_180', 'rule_scope': 'adhikara', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'anta__6_2_180', 'rule_scope': 'adhikara', 'fires': False}),
    "6.2.181": ({'accent_domain': '6.2', 'accent_rule': 'nivibhym', 'accent_blocked': True}, {'accent_domain': '6.2', 'accent_rule': 'nivibhym', 'accent_blocked': False}),
    "6.2.182": ({'accent_domain': '6.2', 'accent_rule': 'pare_abhitobhvi_maalam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'pare_abhitobhvi_maalam', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.183": ({'accent_domain': '6.2', 'accent_rule': 'prt_asvgam_sajym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'prt_asvgam_sajym', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.184": ({'accent_domain': '6.2', 'accent_rule': 'nirudakdni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'nirudakdni', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.185": ({'accent_domain': '6.2', 'accent_rule': 'abhe_mukham', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'abhe_mukham', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.186": ({'accent_domain': '6.2', 'accent_rule': 'apt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'apt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.187": ({'accent_domain': '6.2', 'accent_rule': 'sphigaptavjodhvakukisranmanma', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'sphigaptavjodhvakukisranmanma', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.188": ({'accent_domain': '6.2', 'accent_rule': 'adhe_uparistham', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'adhe_uparistham', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.189": ({'accent_domain': '6.2', 'accent_rule': 'ano_apradhnakanyas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ano_apradhnakanyas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.190": ({'accent_domain': '6.2', 'accent_rule': 'purua_anvdia', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'purua_anvdia', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.191": ({'accent_domain': '6.2', 'accent_rule': 'ate_aktpade', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ate_aktpade', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.192": ({'accent_domain': '6.2', 'accent_rule': 'ne_anidhne', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'ne_anidhne', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.193": ({'accent_domain': '6.2', 'accent_rule': 'tatpuruṣa_prate_avdaya', 'compound_type': 'tatpuruṣa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'tatpuruṣa_prate_avdaya', 'compound_type': 'tatpuruṣa', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.194": ({'accent_domain': '6.2', 'accent_rule': 'upt_dvyajajinam_agaurdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'upt_dvyajajinam_agaurdaya', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.195": ({'accent_domain': '6.2', 'accent_rule': 'so_avakepae', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'so_avakepae', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.196": ({'accent_domain': '6.2', 'accent_rule': 'vibh_utpucche', 'optional': True}, {'accent_domain': '6.2', 'accent_rule': 'vibh_utpucche', 'optional': False}),
    "6.2.197": ({'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_dvitribhym_pddanmrdhasu', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'bahuvrīhi_dvitribhym_pddanmrdhasu', 'compound_type': 'bahuvrīhi', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.198": ({'accent_domain': '6.2', 'accent_rule': 'saktham_akrntt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'saktham_akrntt', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
    "6.2.199": ({'accent_domain': '6.2', 'accent_rule': 'chandas_pardi_bahulam', 'compound_type': 'chandas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': True}, {'accent_domain': '6.2', 'accent_rule': 'chandas_pardi_bahulam', 'compound_type': 'chandas', 'pada_role': 'pūrvapada', 'accent_pattern': 'pūrvapada_udātta', 'fires': False}),
}

META: dict[str, SutraMeta] = {
    "6.2.1": SutraMeta('vidhi', 'बहुव्रीहौ प्रकृत्या पूर्वपदम्', ("accent:6.2", 'bahuvrīhi_prakṛtyā_pūrvapada')),
    "6.2.2": SutraMeta('vidhi', 'तत्पुरुषे तुल्यार्थतृतीयासप्तम्युपमानाव्ययद्वितीयाकृत्याः', ("accent:6.2", 'tatpuruṣa_tulyrthattysaptamyupamnvyayadvitykty')),
    "6.2.3": SutraMeta('vidhi', 'वर्णः वर्णेष्वनेते', ("accent:6.2", 'vara_vareu_anete')),
    "6.2.4": SutraMeta('vidhi', 'गाधलवणयोः प्रमाणे', ("accent:6.2", 'gdhalavaayo_prame')),
    "6.2.5": SutraMeta('vidhi', 'दायाद्यं दायादे', ("accent:6.2", 'dydyam_dyde')),
    "6.2.6": SutraMeta('vidhi', 'प्रतिबन्धि चिरकृच्छ्रयोः', ("accent:6.2", 'pratibandhi_cirakcchrayo')),
    "6.2.7": SutraMeta('vidhi', 'पदेऽपदेशे', ("accent:6.2", 'pade_apadee')),
    "6.2.8": SutraMeta('vidhi', 'निवाते वातत्राणे', ("accent:6.2", 'nivte_vtatre')),
    "6.2.9": SutraMeta('vidhi', 'शारदेअनार्तवे', ("accent:6.2", 'rade_anrtave')),
    "6.2.10": SutraMeta('vidhi', 'अध्वर्युकषाययोर्जातौ', ("accent:6.2", 'adhvaryukayayo_jtau')),
    "6.2.11": SutraMeta('vidhi', 'सदृशप्रतिरूपयोः सादृश्ये', ("accent:6.2", 'sadapratirpayo_sdye')),
    "6.2.12": SutraMeta('vidhi', 'द्विगौ प्रमाणे', ("accent:6.2", 'dvigu_prame')),
    "6.2.13": SutraMeta('vidhi', 'गन्तव्यपण्यं वाणिजे', ("accent:6.2", 'gantavyapayam_vije')),
    "6.2.14": SutraMeta('vidhi', 'मात्रोपज्ञोपक्रमच्छाये नपुंसके', ("accent:6.2", 'mtropajopakramacchye_napusake')),
    "6.2.15": SutraMeta('vidhi', 'सुखप्रिययोर्हिते', ("accent:6.2", 'sukhapriyayo_hite')),
    "6.2.16": SutraMeta('vidhi', 'प्रीतौ च', ("accent:6.2", 'prtau')),
    "6.2.17": SutraMeta('vidhi', 'स्वं स्वामिनि', ("accent:6.2", 'svam_svmini')),
    "6.2.18": SutraMeta('vidhi', 'पत्यावैश्वर्ये', ("accent:6.2", 'patyau_aivarye')),
    "6.2.19": SutraMeta('pratisedha', 'न भूवाक्चिद्दिधिषु', ("accent:6.2", 'bhvkciddidhiu')),
    "6.2.20": SutraMeta('vidhi', 'वा भुवनम्', ("accent:6.2", 'bhuvanam')),
    "6.2.21": SutraMeta('vidhi', 'आशङ्काबाधनेदीयस्सु संभावने', ("accent:6.2", 'akbdhanedyassu_sabhvane')),
    "6.2.22": SutraMeta('vidhi', 'पूर्वे भूतपूर्वे', ("accent:6.2", 'prve_bhtaprve')),
    "6.2.23": SutraMeta('vidhi', 'सविधसनीडसमर्यादसवेशसदेशेषु सामीप्ये', ("accent:6.2", 'savidhasanasamarydasaveasadeeu_smpye')),
    "6.2.24": SutraMeta('vidhi', 'विस्पष्टादीनि गुणवचनेषु', ("accent:6.2", 'vispadni_guavacaneu')),
    "6.2.25": SutraMeta('vidhi', 'श्रज्याऽवमकन्पापवत्सु भावे कर्मधारये', ("accent:6.2", 'karmadhāraya_rajyvamakanppavatsu_bhve')),
    "6.2.26": SutraMeta('vidhi', 'कुमारश्च', ("accent:6.2", 'kumra')),
    "6.2.27": SutraMeta('vidhi', 'आदिः प्रत्येनसि', ("accent:6.2", 'di_pratyenasi')),
    "6.2.28": SutraMeta('vidhi', 'पूगेष्वन्यतरस्याम्', ("accent:6.2", 'pgeu_anyatarasym')),
    "6.2.29": SutraMeta('vidhi', 'इगन्तकालकपालभगालशरावेषु द्विगौ', ("accent:6.2", 'dvigu_igantaklakaplabhaglaarveu')),
    "6.2.30": SutraMeta('vidhi', 'बह्वन्यतरस्याम्', ("accent:6.2", 'bahu_anyatarasym')),
    "6.2.31": SutraMeta('vidhi', 'दिष्टिवितस्त्योश्च', ("accent:6.2", 'diivitastyo')),
    "6.2.32": SutraMeta('vidhi', 'सप्तमी सिद्धशुष्कपक्वबन्धेष्वकालात्\u200c', ("accent:6.2", 'saptam_siddhaukapakvabandheu_aklt')),
    "6.2.33": SutraMeta('vidhi', 'परिप्रत्युपापा वर्ज्यमानाहोरात्रावयवेषु', ("accent:6.2", 'paripratyupp_varjyamnhortrvayaveu')),
    "6.2.34": SutraMeta('vidhi', 'राजन्यबहुवचनद्वंद्वेऽन्धकवृष्णिषु', ("accent:6.2", 'rjanyabahuvacanadvandve_andhakaviu')),
    "6.2.35": SutraMeta('paribhasha', 'संख्या', ("accent:6.2", 'sakhy')),
    "6.2.36": SutraMeta('vidhi', 'आचार्योपसर्जनश्चान्तेवासी', ("accent:6.2", 'cryopasarjana_antevs')),
    "6.2.37": SutraMeta('vidhi', 'कार्तकौजपादयश्च', ("accent:6.2", 'krttakaujapdaya')),
    "6.2.38": SutraMeta('vidhi', 'महान् व्रीह्यपराह्णगृष्टीष्वासजाबालभारभारतहैलिहिलरौरवप्रवृद्धेषु', ("accent:6.2", 'mahn_vrhyaparhagvsajblabhrabhratahailihilarauravapravddh')),
    "6.2.39": SutraMeta('vidhi', 'क्षुल्लकश्च वैश्वदेवे', ("accent:6.2", 'kullaka_vaivadeve')),
    "6.2.40": SutraMeta('vidhi', 'उष्ट्रः सादिवाम्योः', ("accent:6.2", 'ura_sdivmyo')),
    "6.2.41": SutraMeta('vidhi', 'गौः सादसादिसारथिषु', ("accent:6.2", 'gau_sdasdisrathiu')),
    "6.2.42": SutraMeta('vidhi', 'कुरुगार्हपतरिक्तगुर्वसूतजरत्यश्लीलदृढरूपापारेवडवातैतिलकद्रूःपण्यकम्बलो दासीभाराणां च', ("accent:6.2", 'kurugrhapata_luptaprathamntanirdea_riktaguru')),
    "6.2.43": SutraMeta('vidhi', 'चतुर्थी तदर्थे', ("accent:6.2", 'caturth_tadarthe')),
    "6.2.44": SutraMeta('vidhi', 'अर्थे', ("accent:6.2", 'arthe')),
    "6.2.45": SutraMeta('vidhi', 'क्ते च', ("accent:6.2", 'kte')),
    "6.2.46": SutraMeta('vidhi', 'कर्मधारयेऽनिष्ठा', ("accent:6.2", 'karmadhāraya_anih')),
    "6.2.47": SutraMeta('vidhi', 'अहीने द्वितीया', ("accent:6.2", 'ahne_dvity')),
    "6.2.48": SutraMeta('vidhi', 'तृतीया कर्मणि', ("accent:6.2", 'tty_karmai')),
    "6.2.49": SutraMeta('vidhi', 'गतिरनन्तरः', ("accent:6.2", 'gati_anantara')),
    "6.2.50": SutraMeta('vidhi', 'तादौ च निति कृत्यतौ', ("accent:6.2", 'tdau_niti_kti')),
    "6.2.51": SutraMeta('vidhi', 'तवै चान्तश्च युगपत्\u200c', ("accent:6.2", 'tavai_luptaprathamntanirdea_anta')),
    "6.2.52": SutraMeta('vidhi', 'अनिगन्तोऽञ्चतौ वप्रत्यये', ("accent:6.2", 'aniganta_acatau_vapratyaye')),
    "6.2.53": SutraMeta('vidhi', 'न्यधी च', ("accent:6.2", 'nyadh')),
    "6.2.54": SutraMeta('vidhi', 'ईषदन्यतरस्याम्', ("accent:6.2", 'at_anyatarasym')),
    "6.2.55": SutraMeta('vidhi', 'हिरण्यपरिमाणं धने', ("accent:6.2", 'hirayaparimam_dhane')),
    "6.2.56": SutraMeta('vidhi', 'प्रथमोऽचिरोपसम्पत्तौ', ("accent:6.2", 'prathama_aciropasampattau')),
    "6.2.57": SutraMeta('vidhi', 'कतरकतमौ कर्मधारये', ("accent:6.2", 'karmadhāraya_katarakatamau')),
    "6.2.58": SutraMeta('vidhi', 'आर्यो ब्राह्मणकुमारयोः', ("accent:6.2", 'rya_brhmaakumrayo')),
    "6.2.59": SutraMeta('vidhi', 'राजा च', ("accent:6.2", 'rj')),
    "6.2.60": SutraMeta('vidhi', 'षष्ठी प्रत्येनसि', ("accent:6.2", 'ah_pratyenasi')),
    "6.2.61": SutraMeta('vidhi', 'क्ते नित्यार्थे', ("accent:6.2", 'kte_nityrthe')),
    "6.2.62": SutraMeta('vidhi', 'ग्रामः शिल्पिनि', ("accent:6.2", 'grma_ilpini')),
    "6.2.63": SutraMeta('vidhi', 'राजा च प्रशंसायाम्', ("accent:6.2", 'rj_praasym')),
    "6.2.64": SutraMeta('vidhi', 'आदिरुदात्तः', ("accent:6.2", 'di_udtta')),
    "6.2.65": SutraMeta('vidhi', 'सप्तमीहारिणौ धर्म्येऽहरणे', ("accent:6.2", 'saptamhriau_dharmye_aharae')),
    "6.2.66": SutraMeta('vidhi', 'युक्ते च', ("accent:6.2", 'yukte')),
    "6.2.67": SutraMeta('vibhasha', 'विभाषाऽध्यक्षे', ("accent:6.2", 'vibh_adhyake')),
    "6.2.68": SutraMeta('vidhi', 'पापं च शिल्पिनि', ("accent:6.2", 'ppam_ilpini')),
    "6.2.69": SutraMeta('vidhi', 'गोत्रान्तेवासिमाणवब्राह्मणेषु क्षेपे', ("accent:6.2", 'gotrntevsimavabrhmaeu_kepe')),
    "6.2.70": SutraMeta('vidhi', 'अङ्गानि मैरेये', ("accent:6.2", 'agni_maireye')),
    "6.2.71": SutraMeta('vidhi', 'भक्ताख्यास्तदर्थेषु', ("accent:6.2", 'bhaktkhy_tadartheu')),
    "6.2.72": SutraMeta('vidhi', 'गोबिडालसिंहसैन्धवेषूपमाने', ("accent:6.2", 'gobilasihasaindhaveu_upamne')),
    "6.2.73": SutraMeta('vidhi', 'अके जीविकाऽर्थे', ("accent:6.2", 'ake_jvikrthe')),
    "6.2.74": SutraMeta('vidhi', 'प्राचां क्रीडायाम्', ("accent:6.2", 'prcm_krym')),
    "6.2.75": SutraMeta('vidhi', 'अणि नियुक्ते', ("accent:6.2", 'ai_niyukte')),
    "6.2.76": SutraMeta('vidhi', 'शिल्पिनि चाकृञः', ("accent:6.2", 'ilpini_aka')),
    "6.2.77": SutraMeta('vidhi', 'संज्ञायां च', ("accent:6.2", 'sajym')),
    "6.2.78": SutraMeta('vidhi', 'गोतन्तियवं पाले', ("accent:6.2", 'gotantiyavam_ple')),
    "6.2.79": SutraMeta('vidhi', 'णिनि', ("accent:6.2", 'ini')),
    "6.2.80": SutraMeta('vidhi', 'उपमानं शब्दार्थप्रकृतावेव', ("accent:6.2", 'upamnam_abdrthapraktau')),
    "6.2.81": SutraMeta('vidhi', 'युक्तारोह्यादयश्च', ("accent:6.2", 'yuktrohydaya')),
    "6.2.82": SutraMeta('vidhi', 'दीर्घकाशतुषभ्राष्ट्रवटं जे', ("accent:6.2", 'drghakatuabhrravaam_je')),
    "6.2.83": SutraMeta('vidhi', 'अन्त्यात्\u200c पूर्वं बह्वचः', ("accent:6.2", 'antyt_prvam_bahvaca')),
    "6.2.84": SutraMeta('vidhi', 'ग्रामेऽनिवसन्तः', ("accent:6.2", 'grme_anivasanta')),
    "6.2.85": SutraMeta('vidhi', 'घोषादिषु', ("accent:6.2", 'ghodiu_lym')),
    "6.2.86": SutraMeta('vidhi', 'छात्र्यादयः शालायाम्', ("accent:6.2", 'chtrydaya_lym')),
    "6.2.87": SutraMeta('vidhi', 'प्रस्थेऽवृद्धमकर्क्यादीनाम्\u200c', ("accent:6.2", 'prasthe_avddham_akarkydnm')),
    "6.2.88": SutraMeta('vidhi', 'मालाऽऽदीनां च', ("accent:6.2", 'mldnm')),
    "6.2.89": SutraMeta('vidhi', 'अमहन्नवं नगरेऽनुदीचाम्', ("accent:6.2", 'amahannavam_nagare_anudcm')),
    "6.2.90": SutraMeta('vidhi', 'अर्मे चावर्णं द्व्यच्त्र्यच्', ("accent:6.2", 'arme_avaram_dvyac')),
    "6.2.91": SutraMeta('pratisedha', 'न भूताधिकसंजीवमद्राश्मकज्जलम्', ("accent:6.2", 'bhtdhikasajvamadrmakajjalam')),
    "6.2.92": SutraMeta('paribhasha', 'अन्तः', ("accent:6.2", 'anta')),
    "6.2.93": SutraMeta('vidhi', 'सर्वं गुणकार्त्स्न्ये', ("accent:6.2", 'sarvam_guakrtsnye')),
    "6.2.94": SutraMeta('vidhi', 'संज्ञायां गिरिनिकाययोः', ("accent:6.2", 'sajym_girinikyayo')),
    "6.2.95": SutraMeta('vidhi', 'कुमार्यां वयसि', ("accent:6.2", 'kumrym_vayasi')),
    "6.2.96": SutraMeta('vidhi', 'उदकेऽकेवले', ("accent:6.2", 'udake_akevale')),
    "6.2.97": SutraMeta('vidhi', 'द्विगौ क्रतौ', ("accent:6.2", 'dvigu_kratau')),
    "6.2.98": SutraMeta('vidhi', 'सभायां नपुंसके', ("accent:6.2", 'sabhym_napusake')),
    "6.2.99": SutraMeta('vidhi', 'पुरे प्राचाम्', ("accent:6.2", 'pure_prcm')),
    "6.2.100": SutraMeta('vidhi', 'अरिष्टगौडपूर्वे च', ("accent:6.2", 'ariagauaprve')),
    "6.2.101": SutraMeta('pratisedha', 'न हास्तिनफलकमार्देयाः', ("accent:6.2", 'hstinaphalakamrdey')),
    "6.2.102": SutraMeta('vidhi', 'कुसूलकूपकुम्भशालं बिले', ("accent:6.2", 'kuslakpakumbhalam_bile')),
    "6.2.103": SutraMeta('vidhi', 'दिक्\u200cशब्दा ग्रामजनपदाख्यानचानराटेषु', ("accent:6.2", 'dikabd_grmajanapadkhynacnareu')),
    "6.2.104": SutraMeta('vidhi', 'आचार्योपसर्जनश्चान्तेवासिनि', ("accent:6.2", 'cryopasarjana_sup_sthne')),
    "6.2.105": SutraMeta('vidhi', 'उत्तरपदवृद्धौ सर्वं च', ("accent:6.2", 'uttarapadavddhau_sarvam')),
    "6.2.106": SutraMeta('vidhi', 'बहुव्रीहौ विश्वं संज्ञयाम्', ("accent:6.2", 'bahuvrīhi_vivam_sajaym')),
    "6.2.107": SutraMeta('vidhi', 'उदराश्वेषुषु', ("accent:6.2", 'udarveuu')),
    "6.2.108": SutraMeta('vidhi', 'क्षेपे', ("accent:6.2", 'kepe')),
    "6.2.109": SutraMeta('vidhi', 'नदी बन्धुनि', ("accent:6.2", 'nad_bandhuni')),
    "6.2.110": SutraMeta('vidhi', 'निष्ठोपसर्गपूर्वमन्यतरस्याम्\u200c', ("accent:6.2", 'nih_upasargaprvam_anyatarasym')),
    "6.2.111": SutraMeta('vidhi', 'उत्तरपदादिः', ("accent:6.2", 'uttarapaddi')),
    "6.2.112": SutraMeta('vidhi', 'कर्णो वर्णलक्षणात्\u200c', ("accent:6.2", 'kara_varalakat')),
    "6.2.113": SutraMeta('vidhi', 'संज्ञौपम्ययोश्च', ("accent:6.2", 'sajaupamyayo')),
    "6.2.114": SutraMeta('vidhi', 'कण्ठपृष्ठग्रीवाजंघं च', ("accent:6.2", 'kahaphagrvjagham')),
    "6.2.115": SutraMeta('vidhi', 'शृङ्गमवस्थायां च', ("accent:6.2", 'gam_avasthym')),
    "6.2.116": SutraMeta('vidhi', 'नञो जरमरमित्रमृताः', ("accent:6.2", 'naa_jaramaramitramt')),
    "6.2.117": SutraMeta('vidhi', 'सोर्मनसी अलोमोषसी', ("accent:6.2", 'so_manas_alomoas')),
    "6.2.118": SutraMeta('vidhi', 'क्रत्वादयश्च', ("accent:6.2", 'kratvdaya')),
    "6.2.119": SutraMeta('vidhi', 'आद्युदात्तं द्व्यच् छन्दसि', ("accent:6.2", 'chandas_dyudttam_dvyac')),
    "6.2.120": SutraMeta('vidhi', 'वीरवीर्यौ च', ("accent:6.2", 'vravryau')),
    "6.2.121": SutraMeta('vidhi', 'कूलतीरतूलमूलशालाऽक्षसममव्ययीभावे', ("accent:6.2", 'avyayībhāva_klatratlamlalkasamam')),
    "6.2.122": SutraMeta('vidhi', 'कंसमन्थशूर्पपाय्यकाण्डं द्विगौ', ("accent:6.2", 'dvigu_kasamantharpapyyakam')),
    "6.2.123": SutraMeta('vidhi', 'तत्पुरुषे शालायां नपुंसके', ("accent:6.2", 'tatpuruṣa_lym_napusake')),
    "6.2.124": SutraMeta('vidhi', 'कन्था च', ("accent:6.2", 'kanth')),
    "6.2.125": SutraMeta('vidhi', 'आदिश्चिहणादीनाम्', ("accent:6.2", 'di_cihadnm')),
    "6.2.126": SutraMeta('vidhi', 'चेलखेटकटुककाण्डं गर्हायाम्', ("accent:6.2", 'celakheakaukakam_garhym')),
    "6.2.127": SutraMeta('vidhi', 'चीरमुपमानम्\u200c', ("accent:6.2", 'cram_upamnam')),
    "6.2.128": SutraMeta('vidhi', 'पललसूपशाकं मिश्रे', ("accent:6.2", 'palalaspakam_mire')),
    "6.2.129": SutraMeta('vidhi', 'कूलसूदस्थलकर्षाः संज्ञायाम्', ("accent:6.2", 'klasdasthalakar_sajym')),
    "6.2.130": SutraMeta('vidhi', 'अकर्मधारये राज्यम्', ("accent:6.2", 'akarmadhāraya_rjyam')),
    "6.2.131": SutraMeta('vidhi', 'वर्ग्यादयश्च', ("accent:6.2", 'vargydaya')),
    "6.2.132": SutraMeta('vidhi', 'पुत्रः पुंभ्यः', ("accent:6.2", 'putra_pumbhya')),
    "6.2.133": SutraMeta('pratisedha', 'नाचार्यराजर्त्विक्संयुक्तज्ञात्याख्येभ्यः', ("accent:6.2", 'cryarjartviksayuktajtykhyebhya')),
    "6.2.134": SutraMeta('vidhi', 'चूर्णादीन्यप्राणिषष्ठ्याः', ("accent:6.2", 'crdni_apriahy')),
    "6.2.135": SutraMeta('vidhi', 'षट् च काण्डादीनि', ("accent:6.2", 'a_kdni')),
    "6.2.136": SutraMeta('vidhi', 'कुण्डं वनम्', ("accent:6.2", 'kuam_vanam')),
    "6.2.137": SutraMeta('vidhi', 'प्रकृत्या भगालम्', ("accent:6.2", 'prakty_bhaglam')),
    "6.2.138": SutraMeta('vidhi', 'शितेर्नित्याबह्वज्बहुव्रीहावभसत्\u200c', ("accent:6.2", 'bahuvrīhi_ite_nitybahvavc_abhasat')),
    "6.2.139": SutraMeta('vidhi', 'गतिकारकोपपदात्\u200c कृत्\u200c', ("accent:6.2", 'gatikrakopapadt_kt')),
    "6.2.140": SutraMeta('vidhi', 'उभे वनस्पत्यादिषु युगपत्\u200c', ("accent:6.2", 'ubhe_vanaspatydiu')),
    "6.2.141": SutraMeta('vidhi', 'देवताद्वंद्वे च', ("accent:6.2", 'devatdvandve')),
    "6.2.142": SutraMeta('pratisedha', 'नोत्तरपदेऽनुदात्तादावपृथिवीरुद्रपूषमन्थिषु', ("accent:6.2", 'uttarapade_anudttdau_apthivrudrapamanthiu')),
    "6.2.143": SutraMeta('paribhasha', 'अन्तः', ("accent:6.2", 'anta__6_2_143')),
    "6.2.144": SutraMeta('vidhi', 'थाथघञ्क्ताजबित्रकाणाम्', ("accent:6.2", 'ththaghaktjabitrakm')),
    "6.2.145": SutraMeta('vidhi', 'सूपमानात्\u200c क्तः', ("accent:6.2", 'spamnt_kta')),
    "6.2.146": SutraMeta('vidhi', 'संज्ञायामनाचितादीनाम्\u200c', ("accent:6.2", 'sajym_ancitdnm')),
    "6.2.147": SutraMeta('vidhi', 'प्रवृद्धादीनां च', ("accent:6.2", 'pravddhdnm')),
    "6.2.148": SutraMeta('vidhi', 'कारकाद्दत्तश्रुतयोरेवाशिषि', ("accent:6.2", 'krakt_dattarutayo_ii')),
    "6.2.149": SutraMeta('vidhi', 'इत्थम्भूतेन कृतमिति च', ("accent:6.2", 'itthambhtena_ktam')),
    "6.2.150": SutraMeta('vidhi', 'अनो भावकर्मवचनः', ("accent:6.2", 'ana_bhvakarmavacana')),
    "6.2.151": SutraMeta('vidhi', 'मन्क्तिन्व्याख्यानशयनासनस्थानयाजकादिक्रीताः', ("accent:6.2", 'manktinvykhynaayansanasthnayjakdikrt')),
    "6.2.152": SutraMeta('vidhi', 'सप्तम्याः पुण्यम्', ("accent:6.2", 'saptamy_puyam')),
    "6.2.153": SutraMeta('vidhi', 'ऊनार्थकलहं तृतीयायाः', ("accent:6.2", 'nrthakalaham_ttyy')),
    "6.2.154": SutraMeta('vidhi', 'मिश्रं चानुपसर्गमसंधौ', ("accent:6.2", 'miram_anupasargam_asandhau')),
    "6.2.155": SutraMeta('vidhi', 'नञो गुणप्रतिषेधे सम्पाद्यर्हहितालमर्थास्तद्धिताः', ("accent:6.2", 'naa_guapratiedhe_sampdyarhahitlamarth')),
    "6.2.156": SutraMeta('vidhi', 'ययतोश्चातदर्थे', ("accent:6.2", 'yayato_atadarthe')),
    "6.2.157": SutraMeta('vidhi', 'अच्कावशक्तौ', ("accent:6.2", 'ackau_aaktau')),
    "6.2.158": SutraMeta('vidhi', 'आक्रोशे च', ("accent:6.2", 'kroe')),
    "6.2.159": SutraMeta('vidhi', 'संज्ञायाम्', ("accent:6.2", 'sajym__6_2_159')),
    "6.2.160": SutraMeta('vidhi', 'कृत्योकेष्णुच्चार्वादयश्च', ("accent:6.2", 'ktyokeuccrvdaya')),
    "6.2.161": SutraMeta('vibhasha', 'विभाषा तृन्नन्नतीक्ष्णशुचिषु', ("accent:6.2", 'vibh_tnnannatkauciu')),
    "6.2.162": SutraMeta('vidhi', 'बहुव्रीहाविदमेतत्तद्भ्यः प्रथमपूरणयोः क्रियागणने', ("accent:6.2", 'bahuvrīhi_idametattadbhya_prathamapraayo_kriygaane')),
    "6.2.163": SutraMeta('vidhi', 'संख्यायाः स्तनः', ("accent:6.2", 'sakhyy_stana')),
    "6.2.164": SutraMeta('vibhasha', 'विभाषा छन्दसि', ("accent:6.2", 'chandas_vibh')),
    "6.2.165": SutraMeta('vidhi', 'संज्ञायां मित्राजिनयोः', ("accent:6.2", 'sajym_mitrjinayo')),
    "6.2.166": SutraMeta('vidhi', 'व्यवायिनोऽन्तरम्', ("accent:6.2", 'vyavyina_antaram')),
    "6.2.167": SutraMeta('vidhi', 'मुखं स्वाङ्गम्', ("accent:6.2", 'mukham_svgam')),
    "6.2.168": SutraMeta('pratisedha', 'नाव्ययदिक्\u200cशब्दगोमहत्स्थूलमुष्टिपृथुवत्सेभ्यः', ("accent:6.2", 'avyayadikabdagomahatsthlamuipthuvatsebhya')),
    "6.2.169": SutraMeta('vidhi', 'निष्ठोपमानादन्यतरस्याम्', ("accent:6.2", 'nihopamnt_anyatarasym')),
    "6.2.170": SutraMeta('vidhi', 'जातिकालसुखादिभ्योऽनाच्छादनात्\u200c क्तोऽकृतमितप्रतिपन्नाः', ("accent:6.2", 'jtiklasukhdibhya_ancchdant_kta')),
    "6.2.171": SutraMeta('vidhi', 'वा जाते', ("accent:6.2", 'jte')),
    "6.2.172": SutraMeta('vidhi', 'नञ्सुभ्याम्', ("accent:6.2", 'nasubhym')),
    "6.2.173": SutraMeta('vidhi', 'कपि पूर्वम्', ("accent:6.2", 'kapi_prvam')),
    "6.2.174": SutraMeta('vidhi', 'ह्रस्वान्तेऽन्त्यात्\u200c पूर्वम्', ("accent:6.2", 'hrasvnte_antyt_prvam')),
    "6.2.175": SutraMeta('vidhi', 'बहोर्नञ्वदुत्तरपदभूम्नि', ("accent:6.2", 'baho_navat_uttarapadabhmni')),
    "6.2.176": SutraMeta('pratisedha', 'न गुणादयोऽवयवाः', ("accent:6.2", 'gudaya_avayav')),
    "6.2.177": SutraMeta('vidhi', 'उपसर्गात्\u200c स्वाङ्गं ध्रुवमपर्शु', ("accent:6.2", 'upasargt_svgam_dhruvam')),
    "6.2.178": SutraMeta('vidhi', 'वनं समासे', ("accent:6.2", 'samāsa_vanam')),
    "6.2.179": SutraMeta('paribhasha', 'अन्तः', ("accent:6.2", 'anta__6_2_179')),
    "6.2.180": SutraMeta('paribhasha', 'अन्तश्च', ("accent:6.2", 'anta__6_2_180')),
    "6.2.181": SutraMeta('pratisedha', 'न निविभ्याम्', ("accent:6.2", 'nivibhym')),
    "6.2.182": SutraMeta('vidhi', 'परेरभितोभाविमण्डलम्', ("accent:6.2", 'pare_abhitobhvi_maalam')),
    "6.2.183": SutraMeta('vidhi', 'प्रादस्वाङ्गं संज्ञायाम्', ("accent:6.2", 'prt_asvgam_sajym')),
    "6.2.184": SutraMeta('vidhi', 'निरुदकादीनि च', ("accent:6.2", 'nirudakdni')),
    "6.2.185": SutraMeta('vidhi', 'अभेर्मुखम्', ("accent:6.2", 'abhe_mukham')),
    "6.2.186": SutraMeta('vidhi', 'अपाच्च', ("accent:6.2", 'apt')),
    "6.2.187": SutraMeta('vidhi', 'स्फिगपूतवीणाऽञ्जोऽध्वकुक्षिसीरनामनाम च', ("accent:6.2", 'sphigaptavjodhvakukisranmanma')),
    "6.2.188": SutraMeta('vidhi', 'अधेरुपरिस्थम्', ("accent:6.2", 'adhe_uparistham')),
    "6.2.189": SutraMeta('vidhi', 'अनोरप्रधानकनीयसी', ("accent:6.2", 'ano_apradhnakanyas')),
    "6.2.190": SutraMeta('vidhi', 'पुरुषश्चान्वादिष्टः', ("accent:6.2", 'purua_anvdia')),
    "6.2.191": SutraMeta('vidhi', 'अतेरकृत्पदे', ("accent:6.2", 'ate_aktpade')),
    "6.2.192": SutraMeta('vidhi', 'नेरनिधाने', ("accent:6.2", 'ne_anidhne')),
    "6.2.193": SutraMeta('vidhi', 'प्रतेरंश्वादयस्तत्पुरुषे', ("accent:6.2", 'tatpuruṣa_prate_avdaya')),
    "6.2.194": SutraMeta('vidhi', 'उपाद् द्व्यजजिनमगौरादयः', ("accent:6.2", 'upt_dvyajajinam_agaurdaya')),
    "6.2.195": SutraMeta('vidhi', 'सोरवक्षेपणे', ("accent:6.2", 'so_avakepae')),
    "6.2.196": SutraMeta('vibhasha', 'विभाषोत्पुच्छे', ("accent:6.2", 'vibh_utpucche')),
    "6.2.197": SutraMeta('vidhi', 'द्वित्रिभ्यां पाद्दन्मूर्धसु बहुव्रीहौ', ("accent:6.2", 'bahuvrīhi_dvitribhym_pddanmrdhasu')),
    "6.2.198": SutraMeta('vidhi', 'सक्थं चाक्रान्तात्\u200c', ("accent:6.2", 'saktham_akrntt')),
    "6.2.199": SutraMeta('vidhi', 'परादिश्छन्दसि बहुलम्', ("accent:6.2", 'chandas_pardi_bahulam')),
}

(
    IMPLEMENTED_IDS,
    has_real_implementation,
    handler_for,
    positive_features,
    negative_features,
) = make_module_api(FIXTURES, globals())

for _sid, (_pos, _neg) in FIXTURES.items():
    assert handler_for(_sid)(_pos), f"positive fixture failed for {_sid}"
    assert not handler_for(_sid)(_neg), f"negative fixture failed for {_sid}"

