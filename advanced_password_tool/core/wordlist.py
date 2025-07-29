# advanced_password_tool/core/wordlist.py

import itertools
import datetime

# default leet mapping
DEFAULT_LEET = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}

def leet_transform(word: str, leet_map: dict = DEFAULT_LEET) -> set:
    """Generate all single or mixed leet transforms for a word."""
    results = {word}
    for ch, sub in leet_map.items():
        if ch in word.lower():
            new = ''.join(sub if c.lower() == ch else c for c in word)
            results.add(new)
    return results

def case_variants(word: str) -> set:
    """Return lowercase, uppercase, titlecase, and mix-first variants."""
    return {
        word.lower(),
        word.upper(),
        word.capitalize(),
    }

def append_years(words: set, start: int, end: int) -> set:
    """Append years and short-year suffixes to each word."""
    years = list(range(start, end + 1))
    short = [str(y)[-2:] for y in years]
    new = set(words)
    for w in words:
        for y in years + short:
            new.add(f"{w}{y}")
    return new

def generate_custom_wordlist(inputs: list, config: dict) -> list:
    """
    inputs: list of base strings
    config: keys: leet(False), casing(False), years(True), year_range([0,13]), symbols('@','!')
    Returns sorted unique list.
    """
    base_set = set(inputs)
    result = set()

    for w in base_set:
        variants = {w}
        if config.get('casing', False):
            variants |= case_variants(w)
        if config.get('leet', False):
            new = set()
            for v in variants:
                new |= leet_transform(v)
            variants |= new
        result |= variants

    if config.get('years', False):
        start, end = config.get('year_range', [2000, datetime.datetime.now().year])
        result = append_years(result, start, end)

    # Optionally append symbol suffixes or prefixes
    syms = config.get('symbols', [])
    if syms:
        with_syms = set()
        for w in result:
            for s in syms:
                with_syms.add(f"{w}{s}")
                with_syms.add(f"{s}{w}")
        result |= with_syms

    # Optionally combine up to 2-word concatenations
    combos = set()
    for a, b in itertools.permutations(result, 2):
        combos.add(a + b)
    result |= combos

    # Return sorted list
    return sorted(result)
