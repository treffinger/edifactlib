# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

LEVEL_FULL_FRAGMENTS: dict[str, str] = {
    "UNOA": r"A-Z0-9 .,\-()/='+:?!\"%&*;<>",
    "UNOB": r"A-Za-z0-9 .,\-()/='+:?!\"%&*;<>",
    "UNOC": r"\x20-\x7E\xA0-\xFF",
    "UNOD": (
        r"\x20-\x7E"
        r"\xA0\xA4\xA7-\xA8\xAD\xB0\xB4\xB8"
        r"\xC1-\xC2\xC4\xC7\xC9\xCB\xCD-\xCE\xD3-\xD4\xD6-\xD7\xDA\xDC-\xDD\xDF"
        r"\xE1-\xE2\xE4\xE7\xE9\xEB\xED-\xEE\xF3-\xF4\xF6-\xF7\xFA\xFC-\xFD"
        r"Ă-ćČ-đĘ-ěĹ-ĺĽ-ľ"
        r"Ł-ńŇ-ňŐ-őŔ-ŕŘ-ś"
        r"Ş-ťŮ-űŹ-žˇ˘-˙˛˝"
    ),
    "UNOE": (r"\x20-\x7E" r"\xA0\xA7\xAD" r"Ё-ЌЎ-яё-ќў-џ№"),
    "UNOF": (r"\x20-\x7E" r"\xA0\xA3\xA6-\xA9\xAB-\xAD\xB0-\xB3\xB7\xBB\xBD" r"ͺ΄-ΆΈ-ΊΌΎ-ΡΣ-ώ" r"―‘-’€₯"),
}

LEVEL_ALPHA_FRAGMENTS: dict[str, str] = {
    "UNOA": r"A-Z .,\-()/='+:?!\"%&*;<>",
    "UNOB": r"A-Za-z .,\-()/='+:?!\"%&*;<>",
    "UNOC": r"\x20-\x2F\x3A-\x7E\xA0-\xFF",
    "UNOD": (
        r"\x20-\x2F\x3A-\x7E"
        r"\xA0\xA4\xA7-\xA8\xAD\xB0\xB4\xB8"
        r"\xC1-\xC2\xC4\xC7\xC9\xCB\xCD-\xCE\xD3-\xD4\xD6-\xD7\xDA\xDC-\xDD\xDF"
        r"\xE1-\xE2\xE4\xE7\xE9\xEB\xED-\xEE\xF3-\xF4\xF6-\xF7\xFA\xFC-\xFD"
        r"Ă-ćČ-đĘ-ěĹ-ĺĽ-ľ"
        r"Ł-ńŇ-ňŐ-őŔ-ŕŘ-ś"
        r"Ş-ťŮ-űŹ-žˇ˘-˙˛˝"
    ),
    "UNOE": (r"\x20-\x2F\x3A-\x7E" r"\xA0\xA7\xAD" r"Ё-ЌЎ-яё-ќў-џ№"),
    "UNOF": (r"\x20-\x2F\x3A-\x7E" r"\xA0\xA3\xA6-\xA9\xAB-\xAD\xB0-\xB3\xB7\xBB\xBD" r"ͺ΄-ΆΈ-ΊΌΎ-ΡΣ-ώ" r"―‘-’€₯"),
}
