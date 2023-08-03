import unicodedata
import re


def change_display_to_name(display):
    s = remove_accent_chars_regex(display)
    s = s.lower()
    s = re.sub(r'[àáâãäåæ]', 'a', s)
    s = re.sub(r'[èéêëē]', 'e', s)
    s = re.sub(r'[ìíîï]', 'i', s)
    s = re.sub(r'[òóôõöøœ]', 'o', s)
    s = re.sub(r'[ùúûüŭ]', 'u', s)
    s = re.sub(r'[šÞ]', 's', s)
    s = re.sub(r'[čç]', 'c', s)
    s = re.sub(r'[ňñ]', 'n', s)
    s = re.sub(r'[ř]', 'r', s)
    s = re.sub(r'[ž]', 'z', s)
    s = re.sub(r'[ð]', 'd', s)
    s = re.sub(r'[ýÿ]', 'y', s)
    for i in range(0, len(s), 1):
        if s[i] == ' ':
            s.replace(s[i], '-')
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    return s[:62]


def remove_accent_chars_regex(x: str):
    nfkd_form = unicodedata.normalize('NFKD', x)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
