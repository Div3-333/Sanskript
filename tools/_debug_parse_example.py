from sanskript.parser import parse_program

for src in [
    "surakṣitam.\ngaṇitam i śūnya.\npunaḥ i nyūnam tri.\n  gaṇitam i i yoga eka.\nantam.\ndarśanam i.",
    "gaṇitam i śūnya.\npunaḥ i nyūnam tri.\n  gaṇitam i i yoga eka.\nantam.\ndarśanam i.",
]:
    try:
        parse_program(src)
        print("OK:", src[:30])
    except Exception as exc:
        print("FAIL:", type(exc).__name__, str(exc)[:80])
