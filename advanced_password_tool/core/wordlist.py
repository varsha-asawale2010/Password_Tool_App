import itertools
import datetime


def generate_custom_wordlist(inputs: list, config: dict) -> list:
    def case_variants(word):
        return {word, word.lower(), word.upper(), word.capitalize()}

    def leet_transform(word):
        subs = str.maketrans("aAeEiIoOsStT", "443311005577")
        return {word.translate(subs)}

    def append_years(words, start, end):
        extended = set()
        for word in words:
            for year in range(start, end + 1):
                extended.add(f"{word}{year}")
        return words | extended

    # Start with base set of user inputs
    base = set(i.strip() for i in inputs if i.strip())
    result = set()

    for word in base:
        variants = {word}
        if config.get('casing'):
            variants |= case_variants(word)
        if config.get('leet'):
            variants |= set().union(*(leet_transform(v) for v in variants))
        result |= variants

    if config.get('years'):
        start, end = config.get('year_range', [2000, datetime.datetime.now().year])
        result = append_years(result, start, end)

    # Add symbols
    symbols = config.get('symbols', ['!', '@', '#'])
    with_syms = set()
    for word in result:
        for sym in symbols:
            with_syms.add(f"{sym}{word}")
            with_syms.add(f"{word}{sym}")
    result |= with_syms

    # Avoid mirrored duplicates like A+B and B+A
    combos = set()
    seen_pairs = set()
    for a, b in itertools.permutations(result, 2):
        if a == b or (b, a) in seen_pairs:
            continue
        seen_pairs.add((a, b))
        combos.add(f"{a}{b}")

    # Final wordlist (no duplicates)
    return sorted(result | combos)
